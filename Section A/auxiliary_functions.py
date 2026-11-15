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

def summary_stats(returns, periods_per_year = 12):
    """
    Annualized summary statistics for a set of excess return series.

    Parameters
    ----------

    returns: pd.DataFrame
        Periodic (e.g. monthly) simple excess returns, one column per asset.

    periods_per_year: int, default 12
        Number of periods in a year (12 for monthly data).

    
    Returns
    -------

    pd.DataFrame
        One row per asset with columns:
        - Annualized Mean: mean * periods_per_year
        - Annualized Volatility: std * sqrt(periods_per_year)
        - Annualized Sharpe: Annualized Mean / Annualized Volatility (no rf subtracted: inputs are already in excess return)
        - Skewness: sample skewness
        - Kurtosis: sample excess kurtosis (normal distribution = 0)
    
    """

    ann_mean = returns.mean() * periods_per_year
    ann_vol = returns.std() * np.sqrt(periods_per_year)

    stats = pd.DataFrame({
        "Annualized Mean": ann_mean,
        "Annualized Volatility": ann_vol,
        "Annualized Sharpe": ann_mean / ann_vol,
        "Skewness": returns.skew(),
        "Kurtosis": returns.kurt()
    })

    return stats

def benchmark_forecast(returns, window = 252, oos_start = "2001-01"):
    """
    Rolling-window historical mean (benchmark) forecast of excess returns.

    The forecast for month 't' is the mean of the previous 'window' months (t - window to t - 1), so it only uses information available before t.

    Parameters
    ----------

    returns: pd.DataFrame
        Monthly simple excess returns, one column per asset, indexed by monthly period.

    window: int, default 252
        Number of past months in each rolling estimate (252 = Jan 1980 - Dec 2000 in-sample period).

    oos_start: str, default '2001-01'
        First out-of-sample month to forecast.

    
    Returns
    -------

    pd.DataFrame
        Monthly benchmark forecasts, indexed by the month being forecast.
    
    """

    # Mean of the last 'window' months, including the current month
    rolling_mean = returns.rolling(window).mean()

    # Shift by one month: the forecast for t uses data up to t - 1 only (no look-ahead)
    forecast = rolling_mean.shift(1)

    # keep only the out-of-sample period
    return forecast.loc[oos_start:]

