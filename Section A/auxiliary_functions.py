# Helper functions for Section A
import numpy as np
import pandas as pd
from pathlib import Path

# Path to the data, built from this file's own location, so it works no matter where the notebook is run from
DATA_DIR = Path(__file__).resolve().parent.parent / "Data on Assets"


def load_series(filename, new_name):
    #Load a 2-column Excel file (date, value) and index it by monthly period.
    df = pd.read_excel(DATA_DIR / filename)
    df.columns = ["date", new_name]
    df["date"] = pd.to_datetime(df["date"]).dt.to_period("M")

    return df.set_index("date")[new_name]