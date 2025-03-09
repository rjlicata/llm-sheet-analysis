import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from sheet_analysis.llm.agent import AnalysisAgent
from sheet_analysis.utils.spreadsheet import load_data


def main():
    """main function for the streamlit app"""
    # define title and initial instructions
    st.title("Spreadsheet Analysis Chatbot")
    subheader = st.empty()
    subheader.subheader("The chat session begins once you upload a file.")
    # define sidebar options
    st.sidebar.title("Upload your CSV/Excel file")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv"])
    model_name = st.sidebar.text_input("Model Name:", value="llama3.2")
    temperature = st.sidebar.slider(
        "Model temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.05,
    )
    show_code = st.sidebar.checkbox("Show Code", value=True)
    # once file is uploaded, create an agent and start chat
    if uploaded_file is not None:
        # update instructions
        subheader.subheader("Ask me anything!")
        # load data and create agent
        data = load_data(uploaded_file, suffix=uploaded_file.name.split(".")[-1])
        agent = AnalysisAgent(
            data=data,
            model_name=model_name,
            temperature=temperature,
            show_code=show_code,
        )
        # display chat messages
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        # chat input at the bottom
        user_input = st.chat_input("Input your query here")
        if user_input:
            # store and display user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            # invoke agent and store and display bot response
            bot_response, code = agent.invoke(user_input)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                st.markdown(bot_response)
            # display the figure if it was generated
            if code.count("plt") > 1:
                st.pyplot(plt.gcf())

    # clear chat option
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []


# run the Streamlit app
if __name__ == "__main__":
    main()
