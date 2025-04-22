import pandas_ta as ta
import pandas as pd

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.reset_index(drop=True)
    df['close'] = df['close'].astype(float)
    df.index = df.index.astype(str)

    df['rsi'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
    if not macd.empty:
        macd.columns = ['macd', 'macds', 'macdh']
        df = pd.concat([df, macd], axis=1)

    df['ema_12'] = ta.ema(df['close'], length=12)
    df['ema_26'] = ta.ema(df['close'], length=26)

    return df
