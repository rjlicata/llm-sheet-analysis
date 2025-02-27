from time import sleep

from sheet_analysis.llm.agent import AnalysisAgent


def conversation(filepath: str, model_name: str = "llama3.2", temperature: float = 0.0) -> None:
    """handles model interface with spreadsheet through user queries

    :param filepath: path to spreadsheet
    :type filepath: str
    :param model_name: Ollama model name to use, defaults to "llama3.2"
    :type model_name: str, optional
    :param temperature: model generation temperature, defaults to 0.0
    :type temperature: float, optional
    """
    agent = AnalysisAgent(
        filepath=filepath,
        model_name=model_name,
        temperature=temperature,
    )
    user_input = ""
    print("Your session with the agent is beginning. To end, enter STOP or hit Ctrl + C")
    sleep(1)
    while True:
        print("-" * 150)
        user_input = input("User Message: ")
        if user_input == "STOP":
            break
        response = agent.invoke(user_input)
        print(f"AI Response: {response}")
        sleep(1)
    print("-" * 150)
    print("Your session has ended. Thank you!")
