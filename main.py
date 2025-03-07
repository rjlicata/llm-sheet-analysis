import streamlit as st

from sheet_analysis.llm.agent import AnalysisAgent


def main(filepath, model_name, temperature):
    agent = AnalysisAgent(
        filepath=filepath,
        model_name=model_name,
        temperature=temperature,
    )
    st.title("Spreadsheet Analysis Chatbot")

    st.subheader("Ask me anything!")

    # Create a text input box for the user
    user_input = st.text_input("You: ", "")

    # Initialize a chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    if user_input:
        # Display the user's message in the chat history
        st.session_state.history.append(f"You: {user_input}")

        # Get a response from the chatbot
        chatbot_response = agent.invoke(user_input)

        # Add the chatbot's response to the chat history
        st.session_state.history.append(f"Bot: {chatbot_response}")

    # Display the chat history
    for message in st.session_state.history:
        st.write(message)


# Run the Streamlit app
if __name__ == "__main__":
    main("data/housing.csv", "llama3.2", 0.0)
