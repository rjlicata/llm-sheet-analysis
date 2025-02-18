from typing import Any, Tuple

from sheet_analysis.utils.coding import run_code
from sheet_analysis.llm.ollama import ModelHandler
from sheet_analysis.llm.prompts import (
    BASIC_SYSTEM_MESSAGE,
    CODE_GEN_SYSTEM_MESSAGE,
    REFACTOR_PROMPT,
)
from sheet_analysis.utils.spreadsheet import load_data


class AnalysisAgent:
    """handles prompting and interaction with the Ollama ModelHandler for code generation;
    also runs the code which is where code safety is handled"""

    def __init__(
        self,
        filepath: str,
        model_name: str = "llama3.2",
        temperature: float = 0.0,
    ):
        """initializes AnalysisAgent

        :param filepath: path to dataset
        :type filepath: str
        :param model_name: Ollama model name to use, defaults to "llama3.2"
        :type model_name: str, optional
        :param temperature: generation temperature for the LLM, defaults to 0.0
        :type temperature: float, optional
        """
        self._data = load_data(filepath)
        self._model = ModelHandler(
            model_name=model_name,
            temperature=temperature,
        )

    def _analyze(self, prompt: str) -> Tuple[str, str, bool]:
        """adds column information to the prompt, invokes the model, and runs the code

        :param prompt: original user query
        :type prompt: str
        :return: code output, code, and error flag
        :rtype: Tuple[str, str, bool]
        """
        prompt = f"The data has the following columns: {self._data.columns}. {prompt}"
        response = self._model.invoke(prompt, sys_msg=CODE_GEN_SYSTEM_MESSAGE)
        error = False
        try:
            result, code = run_code(response, self._data)
        except Exception as e:
            error = True
            result = e
            code = response
        return result, code, error

    def _refactor_output(self, response: Any) -> str:
        """the original code output will be of a numerical or JSONic type, so this
        handles reprompting the model with the code output to get an assistant response
        to the user query

        :param response: code output
        :type response: Any
        :return: assistant response with the output
        :rtype: str
        """
        prompt = REFACTOR_PROMPT.format(response=response)
        return self._model.invoke(prompt, sys_msg=BASIC_SYSTEM_MESSAGE)

    def invoke(self, prompt: str) -> str:
        """invocation of the AnalysisAgent; handles model calling, code processing,
        code running, response refactoring, and error handling

        :param prompt: user query
        :type prompt: str
        :return: final response from the model/code
        :rtype: str
        """
        code_output, code, error_flag = self._analyze(prompt)
        if error_flag:
            return f"I am sorry, I ran into the following error: {code_output}\n\nHere is the code I generated:\n\n{code}"
        if code_output is None and ("savefig" not in code):
            return f"Here is the code I generated:\n\n{code}"
        response = ""
        if code_output is not None:
            model_output = self._refactor_output(code_output)
            response += f"{model_output}\n\n"
        if "savefig" in code:
            response += "I generated a figure for you. It is located at figures/output.png\n\n"
        response += f"Here is the code I generated to get that:\n\n{code}"
        self._model.clear_messages()
        return response
