from openai import OpenAI

from sheet_analysis.llm.prompts import BASIC_SYSTEM_MESSAGE


class ModelHandler:
    """handles basic communication with the Ollama model endpoint"""

    def __init__(
        self,
        model_name: str = "llama3.2",
        system_message: str = BASIC_SYSTEM_MESSAGE,
        temperature: float = 0.7,
    ):
        """initializes ModelHandler

        :param model_name: Ollama model name, defaults to "llama3.2"
        :type model_name: str, optional
        :param system_message: system message for the LLM, defaults to BASIC_SYSTEM_MESSAGE
        :type system_message: str, optional
        :param temperature: generation temperature for the model, defaults to 0.7
        :type temperature: float, optional
        """
        self._client = OpenAI(
            base_url="http://host.docker.internal:11434/v1",
            api_key="ollama",
        )
        self._model_name = model_name
        self._system_message = system_message
        self._temperature = temperature
        self.clear_messages()

    def clear_messages(self) -> None:
        """resets messages with only system message"""
        self._messages = [
            {
                "role": "system",
                "content": self._system_message,
            },
        ]

    def _check_system_message(self, sys_msg: str) -> None:
        """updates the system message with a user-provided one if it is different
        than the one in the message list

        :param sys_msg: system message override
        :type sys_msg: str
        """
        if self._messages[0]["content"] != sys_msg:
            self._messages[0]["content"] = sys_msg

    def invoke(self, user_message: str, sys_msg: str = None) -> str:
        """handles the message list and invokes the LLM

        :param user_message: user query
        :type user_message: str
        :param sys_msg: user override to system message, defaults to None
        :type sys_msg: str, optional
        :return: model response
        :rtype: str
        """
        if sys_msg is not None:
            self._check_system_message(sys_msg)
        self._messages.append(
            {
                "role": "user",
                "content": user_message,
            },
        )
        response = (
            self._client.chat.completions.create(
                messages=self._messages,
                model=self._model_name,
                temperature=self._temperature,
            )
            .choices[0]
            .message.content
        )
        self._messages.append(
            {
                "role": "assistant",
                "content": response,
            },
        )
        return response
