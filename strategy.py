from datetime import datetime

def decide_trade(row, rsi_buy=40, rsi_sell=60):
    rsi = row.get('rsi')
    macd = row.get('macd')
    macds = row.get('macds')
    price = row.get('close')
    timestamp_raw = row.get("timestamp", 0)
    try:
        ts = int(float(timestamp_raw))
    except (ValueError, TypeError):
        ts = 0
    time = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M")

    if rsi is None or macd is None or macds is None:
        return {"signal": "HOLD", "reason": "Missing indicator data", "time": time}
    if rsi < rsi_buy and macd > macds:
        return {"signal": "BUY", "reason": f"RSI below {rsi_buy} and MACD crossover", "time": time}
    elif rsi > rsi_sell and macd < macds:
        return {"signal": "SELL", "reason": f"RSI above {rsi_sell} and MACD crossdown", "time": time}
    else:
        return {"signal": "HOLD", "reason": "No clear signal", "time": time}
