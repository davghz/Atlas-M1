import pandas_ta as ta
import pandas as pd
import numpy as np

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds technical indicators to the input DataFrame.

    The function calculates and adds the following indicators:
    - RSI (Relative Strength Index) with a length of 14.
    - MACD (Moving Average Convergence Divergence) with fast=12, slow=26, signal=9.
      This adds three columns: 'macd', 'macds' (signal line), and 'macdh' (histogram).
    - EMA (Exponential Moving Average) with a length of 12 ('ema_12').
    - EMA (Exponential Moving Average) with a length of 26 ('ema_26').

    The input DataFrame's index is reset, and then converted to string type.
    The 'close' column is cast to float type.

    Args:
        df (pd.DataFrame): Input DataFrame. Must contain a 'close' column with price data.
                           The 'close' column will be converted to float.

    Returns:
        pd.DataFrame: The DataFrame with the added indicator columns.
                      The index of the returned DataFrame will be of string type.
                      If the input DataFrame is empty or lacks a 'close' column,
                      the behavior might depend on the underlying `pandas-ta` library,
                      but it aims to handle it gracefully (e.g., by returning NaNs or an empty DataFrame).
    """
    df = df.reset_index(drop=True)
    df['close'] = df['close'].astype(float)
    df.index = df.index.astype(str)

    df['rsi'] = ta.rsi(df['close'], length=14)
    
    # MACD calculation
    fast_period = 12
    slow_period = 26
    signal_period = 9
    macd_df = ta.macd(df['close'], fast=fast_period, slow=slow_period, signal=signal_period)
    
    if macd_df is not None and not macd_df.empty:
        # pandas-ta typically names columns like MACD_12_26_9, MACDh_12_26_9, MACDs_12_26_9
        # The order is typically MACD, Histogram, Signal
        df['macd'] = macd_df.get(f'MACD_{fast_period}_{slow_period}_{signal_period}')
        df['macdh'] = macd_df.get(f'MACDh_{fast_period}_{slow_period}_{signal_period}') # Histogram
        df['macds'] = macd_df.get(f'MACDs_{fast_period}_{slow_period}_{signal_period}') # Signal line
    else:
        # Ensure columns exist even if MACD calculation fails or returns None/empty
        df['macd'] = np.nan
        df['macdh'] = np.nan
        df['macds'] = np.nan

    df['ema_12'] = ta.ema(df['close'], length=12)
    df['ema_26'] = ta.ema(df['close'], length=26)

    return df
