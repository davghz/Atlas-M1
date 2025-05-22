from datetime import datetime, timezone
import pandas as pd

def decide_trade(row, rsi_buy=40, rsi_sell=60):
    """
    Decides whether to issue a BUY, SELL, or HOLD signal based on technical indicators.

    Args:
        row (pd.Series or dict): A data structure containing the latest market data and indicators.
            Expected keys:
                'rsi' (float, optional): The Relative Strength Index value.
                'macd' (float, optional): The MACD line value.
                'macds' (float, optional): The MACD signal line value.
                'close' (float): The closing price of the asset.
                'timestamp' (int or float, optional): Unix timestamp of the data point.
                                                     Defaults to 0 if missing or invalid,
                                                     resulting in '1970-01-01 00:00' UTC time.
        rsi_buy (int, optional): The RSI threshold below which a BUY signal might be generated.
                                 Defaults to 40.
        rsi_sell (int, optional): The RSI threshold above which a SELL signal might be generated.
                                  Defaults to 60.

    Returns:
        dict: A dictionary containing the trading signal and reasoning.
            Example:
            {
                "signal": "BUY" | "SELL" | "HOLD",
                "reason": "A string explaining why the signal was generated.",
                "time": "YYYY-MM-DD HH:MM" (UTC string representation of the timestamp)
            }
            If essential indicator data ('rsi', 'macd', 'macds') is missing,
            it returns a "HOLD" signal with "Missing indicator data" as the reason.
    """
    rsi = row.get('rsi')
    macd = row.get('macd')
    macds = row.get('macds')
    price = row.get('close')
    timestamp_raw = row.get("timestamp", 0)
    try:
        ts = int(float(timestamp_raw))
    except (ValueError, TypeError):
        ts = 0
    # time = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
    dt_utc = datetime.utcfromtimestamp(ts)
    time = dt_utc.replace(tzinfo=timezone.utc).strftime("%Y-%m-%d %H:%M")

    if rsi is None or pd.isna(rsi) or \
       macd is None or pd.isna(macd) or \
       macds is None or pd.isna(macds):
        return {"signal": "HOLD", "reason": "Missing indicator data", "time": time}

    # All indicators are present and not NaN at this point
    if rsi < rsi_buy and macd > macds:
        return {"signal": "BUY", "reason": f"RSI below {rsi_buy} and MACD crossover", "time": time}
    elif rsi > rsi_sell and macd < macds:
        return {"signal": "SELL", "reason": f"RSI above {rsi_sell} and MACD crossdown", "time": time}
    else: # Indicators are present but no clear buy/sell signal
        return {"signal": "HOLD", "reason": "No clear signal", "time": time}
