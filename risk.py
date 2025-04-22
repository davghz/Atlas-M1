# risk.py

def calculate_position_size(usd_balance, price, risk_pct=0.02):
    """
    Calculate how much BTC to buy based on USD balance and risk percentage.
    Example: 2% risk of $10,000 = $200 position size
    """
    risk_usd = usd_balance * risk_pct
    btc_amount = risk_usd / price if price > 0 else 0
    return round(btc_amount, 8)

def check_max_exposure(current_exposure, max_exposure_pct=1.0):
    """
    Check if we are within allowable exposure limits (e.g. max 100% exposure)
    """
    return current_exposure <= max_exposure_pct
