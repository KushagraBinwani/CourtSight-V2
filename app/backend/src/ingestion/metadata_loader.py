import pandas as pd


def load_metadata(path):

    return pd.read_parquet(path)