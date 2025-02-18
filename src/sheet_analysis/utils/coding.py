import importlib
import os
from typing import Any, Tuple

import pandas as pd

from temp_data import temp_funcs

ALLOWED_PACKAGES = ["pandas", "numpy", "datetime", "re", "sklearn", "scipy", "matplotlib"]


def check_imports(response: str) -> None:
    """finds all lines in the code with imports and checks if they are allowed

    :param response: model response
    :type response: str
    :raises ValueError: code contains an import that is not allowed
    """
    split_response = response.split("\n")
    imports = []
    for line in split_response:
        if len(line) > 0:
            if "import" in line.split(" "):
                imports.append(line)

    for imp in imports:
        if not any([acc in imp for acc in ALLOWED_PACKAGES]):
            raise ValueError(f"Import {imp} is not allowed.")


def remove_end_of_code(response: str) -> str:
    """sometimes the model will still include test code after the function; this
    will stop the code snippet once the function is complete

    :param response: original code snippet
    :type response: str
    :return: updated code snippet
    :rtype: str
    """
    split_response = response.split("\n")
    output = []
    start_flag = False
    for line in split_response:
        if len(line) > 0:
            if start_flag and (line[:4] != "    "):
                break
        if "def" in line:
            start_flag = True
        output.append(line)
    return "\n".join(output)


def write_code(response: str) -> None:
    """writes the code to a file

    :param response: model response
    :type response: str
    """
    temp_data_dir = "temp_data"
    os.makedirs(temp_data_dir, exist_ok=True)

    file_path = os.path.join(temp_data_dir, "temp_funcs.py")
    with open(file_path, "w") as file:
        file.write(response)


def empty_file() -> None:
    """empties the contents of the temporary function file"""
    with open("temp_data/temp_funcs.py", "w") as file:
        file.write("")


def run_code(response: str, data: pd.DataFrame) -> Tuple[Any, str]:
    """performs import check for safety, writes code to file, and runs the code

    :param response: LLM response
    :type response: str
    :param data: data that the LLM code has access to
    :type data: pd.DataFrame
    :return: result of the code and the code block that was run
    :rtype: Tuple[Any, str]
    """
    check_imports(response)
    response = response.split("```python")[1].split("```")[0]
    response = remove_end_of_code(response)
    write_code(response)
    importlib.reload(temp_funcs)

    code_output = temp_funcs.func(data)
    empty_file()
    code_string = f"```python\n{response}\n```"
    return code_output, code_string
