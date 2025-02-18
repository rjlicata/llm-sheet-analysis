import pandas as pd


def load_data(filename: str) -> pd.DataFrame:
    """load spreadsheet data from file

    :param filename: filepath for input data
    :type filename: str
    :return: loaded data
    :rtype: pd.DataFrame
    """
    suffix = filename.split(".")[-1]
    if suffix == "csv":
        return pd.read_csv(filename)
    elif suffix == "xlsx":
        return pd.read_excel(filename)
    raise ValueError("Invalid file format. Must be CSV or XLSX.")
