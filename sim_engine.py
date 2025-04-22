import pandas as pd
from strategy import decide_trade
from risk import calculate_position_size, check_max_exposure
from datetime import datetime, timedelta

class SimulatedWallet:
    def __init__(self, starting_usd=10000.0, fee_rate=0.001, max_exposure_pct=1.0, risk_pct=0.02, tp_pct=0.03, sl_pct=0.01):
        self.usd = starting_usd
        self.btc = 0.0
        self.fee_rate = fee_rate
        self.max_exposure_pct = max_exposure_pct
        self.risk_pct = risk_pct
        self.tp_pct = tp_pct
        self.sl_pct = sl_pct
        self.entry_price = None
        self.entry_time = None
        self.history = []

    def _log(self, time, signal, price, amount, reason):
        value = self.usd + self.btc * price
        self.history.append({
            "time": time,
            "signal": signal,
            "price": price,
            "amount": amount,
            "usd_balance": self.usd,
            "btc_balance": self.btc,
            "portfolio_value": value,
            "reason": reason
        })

    def _should_exit(self, current_price, current_time):
        if self.entry_price is None:
            return False, ""
        price_change_pct = (current_price - self.entry_price) / self.entry_price
        hold_time = current_time - self.entry_time
        if price_change_pct >= self.tp_pct:
            return True, "Take Profit Triggered"
        elif price_change_pct <= -self.sl_pct:
            return True, "Stop Loss Triggered"
        elif hold_time >= timedelta(hours=24):
            return True, "Time-Based Exit (24h)"
        return False, ""

    def execute_trade(self, signal, price, time_str, reason):
        time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        total_value = self.usd + self.btc * price
        current_exposure = (self.btc * price) / total_value if total_value > 0 else 0

        if signal == "BUY" and self.usd > 0 and check_max_exposure(current_exposure, self.max_exposure_pct):
            btc_to_buy = calculate_position_size(self.usd, price, self.risk_pct)
            cost = btc_to_buy * price * (1 + self.fee_rate)
            if self.usd >= cost:
                self.usd -= cost
                self.btc += btc_to_buy
                self.entry_price = price
                self.entry_time = time
                self._log(time_str, "BUY", price, btc_to_buy, reason)
            else:
                self._log(time_str, "HOLD", price, 0, "Insufficient funds for risk-based position")
        elif signal == "SELL" or (self.btc > 0 and self._should_exit(price, time)[0]):
            exit_reason = reason
            if signal != "SELL":
                exit_triggered, exit_reason = self._should_exit(price, time)
                if not exit_triggered:
                    self._log(time_str, "HOLD", price, 0, reason)
                    return
            usd_gained = self.btc * price * (1 - self.fee_rate)
            self.usd += usd_gained
            self._log(time_str, "SELL", price, self.btc, exit_reason)
            self.btc = 0
            self.entry_price = None
            self.entry_time = None
        else:
            self._log(time_str, "HOLD", price, 0, reason)

    def to_dataframe(self):
        return pd.DataFrame(self.history)

def run_simulation(filepath="btc_1h_data_with_indicators.csv"):
    df = pd.read_csv(filepath)
    wallet = SimulatedWallet()
    for _, row in df.dropna().iterrows():
        decision = decide_trade(row)
        wallet.execute_trade(
            signal=decision["signal"],
            price=row["close"],
            time_str=decision["time"],
            reason=decision["reason"]
        )
    results = wallet.to_dataframe()
    results.to_csv("simulated_trades.csv", index=False)
    print("Simulation complete. Results saved to simulated_trades.csv")
    return results

if __name__ == "__main__":
    run_simulation()
