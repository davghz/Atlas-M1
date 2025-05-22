# risk.py

def calculate_position_size(usd_balance, price, risk_pct=0.02):
    """
    Calculates the amount of BTC to buy based on the USD balance, price, and risk percentage.

    Args:
        usd_balance (float): The total USD balance available.
        price (float): The current price of BTC in USD.
        risk_pct (float, optional): The percentage of the USD balance to risk. Defaults to 0.02 (2%).

    Returns:
        float: The amount of BTC to buy, rounded to 8 decimal places.
               Returns 0 if the price is zero.
    Example: 2% risk of $10,000 = $200 position size
    """
    risk_usd = usd_balance * risk_pct
    btc_amount = risk_usd / price if price > 0 else 0
    return round(btc_amount, 8)

def check_max_exposure(current_exposure, max_exposure_pct=1.0):
    """
    Checks if the current exposure is within the allowable maximum exposure limit.

    Args:
        current_exposure (float): The current exposure percentage (e.g., 0.5 for 50%).
        max_exposure_pct (float, optional): The maximum allowable exposure percentage.
                                            Defaults to 1.0 (100%).

    Returns:
        bool: True if current exposure is less than or equal to the maximum exposure, False otherwise.
    """
    return current_exposure <= max_exposure_pct
