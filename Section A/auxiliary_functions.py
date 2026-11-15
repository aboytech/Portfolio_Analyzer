# Helper functions for Section A
import numpy as np
import pandas as pd
from pathlib import Path

# Path to the data, built from this file's own location, so it works no matter where the notebook is run from
DATA_DIR = Path(__file__).resolve().parent.parent / "Data on Assets"


def load_series(filename, new_name):
    """

    Load a 2-column Excel file (date, value) and index it by monthly period.
    
    """
    df = pd.read_excel(DATA_DIR / filename)
    df.columns = ["date", new_name]
    df["date"] = pd.to_datetime(df["date"]).dt.to_period("M")

    return df.set_index("date")[new_name]

def compute_excess_returns(prices, rf):
    """
    Compute monthly simple excess returns.

    Parameters
    ----------

    prices: pd.DataFrame
        Monthly price levels, one column per asset, indexed by monthly period

    rf: pd.Series
        Monthly risk_free rate in decimal form (0.008 = 0.8%), same index.

    
    Returns
    -------

    pd.DataFrame
        Simple excess returns (R_t - rf_t), first (NaN) month removed

    """

    returns = prices.pct_change().dropna()
    excess = returns.sub(rf, axis = 0)

    return excess.dropna()