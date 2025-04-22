from coinbase_client import get_client
from fetch_data import get_account_balances, get_btc_price, get_btc_1h_candles
from indicators import add_indicators
from strategy import decide_trade
from logger import log_trade
import pandas as pd

def main():
    client = get_client()

    # 1. Fetch balances
    balances = get_account_balances(client)
    print("Balances:")
    for currency, value in balances.items():
        print(f"{currency}: {value}")

    # 2. Fetch live BTC price
    price = get_btc_price(client)
    print(f"\nCurrent BTC-USD Price: {price}")

    # 3. Fetch historical candles (up to now)
    candles = get_btc_1h_candles(client)
    df = pd.DataFrame([{
        "timestamp": c.start,
        "low": c.low,
        "high": c.high,
        "open": c.open,
        "close": c.close,
        "volume": c.volume
    } for c in candles.candles])

    # 4. Add indicators
    df = add_indicators(df)

    # 5. Make latest trade decision
    latest = df.dropna().iloc[-1]
    decision = decide_trade(latest)

    # 6. Log decision
    log_trade(decision, balances)
    print(f"\nTrade Signal: {decision['signal']} | Reason: {decision['reason']} | Time: {decision['time']}")

    # 7. Save full data snapshot (optional)
    df.to_csv("btc_1h_data_with_indicators.csv", index=False)

if __name__ == "__main__":
    main()
