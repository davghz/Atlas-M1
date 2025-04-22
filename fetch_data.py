import datetime as dt

def get_now_unix():
    return int(dt.datetime.utcnow().timestamp())

def get_account_balances(client):
    accounts = client.get_accounts()
    return {a.currency: a.available_balance['value'] for a in accounts.accounts}

def get_btc_price(client):
    return client.get_product("BTC-USD").price

def get_btc_1h_candles(client, limit=50):
    now = get_now_unix()
    start = now - (limit * 3600)
    end = now
    return client.get_candles(product_id="BTC-USD", start=start, end=end, granularity="ONE_HOUR")
