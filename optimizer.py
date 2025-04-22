import pandas as pd
from sim_engine import SimulatedWallet
from strategy import decide_trade
from risk import calculate_position_size, check_max_exposure
from datetime import datetime, timedelta

# M1.01 Strategy Configs – Aggressive RSI and Risk Ranges
strategy_configs = [
    {"rsi_buy": 45, "rsi_sell": 55, "tp_pct": 0.03, "sl_pct": 0.01, "risk_pct": 0.03},
    {"rsi_buy": 48, "rsi_sell": 52, "tp_pct": 0.025, "sl_pct": 0.015, "risk_pct": 0.03},
    {"rsi_buy": 50, "rsi_sell": 50, "tp_pct": 0.02, "sl_pct": 0.02, "risk_pct": 0.04},
    {"rsi_buy": 52, "rsi_sell": 48, "tp_pct": 0.015, "sl_pct": 0.015, "risk_pct": 0.05}
]

def run_config_simulation(config, df):
    wallet = SimulatedWallet(
        starting_usd=10000.0,
        fee_rate=0.001,
        max_exposure_pct=1.0,
        risk_pct=config["risk_pct"],
        tp_pct=config["tp_pct"],
        sl_pct=config["sl_pct"]
    )
    for _, row in df.dropna().iterrows():
        decision = decide_trade(row, rsi_buy=config["rsi_buy"], rsi_sell=config["rsi_sell"])
        wallet.execute_trade(
            signal=decision["signal"],
            price=row["close"],
            time_str=decision["time"],
            reason=decision["reason"]
        )
    results = wallet.to_dataframe()
    final_value = results["portfolio_value"].iloc[-1]
    trades = results[results["signal"].isin(["BUY", "SELL"])].shape[0]
    return {
        "rsi_buy": config["rsi_buy"],
        "rsi_sell": config["rsi_sell"],
        "tp_pct": config["tp_pct"],
        "sl_pct": config["sl_pct"],
        "risk_pct": config["risk_pct"],
        "final_value": round(final_value, 2),
        "net_return_pct": round((final_value - 10000) / 10000 * 100, 2),
        "total_trades": trades
    }

def run_optimizer(data_path="btc_1h_data_with_indicators.csv", output_path="optimizer_results.csv"):
    df = pd.read_csv(data_path)
    all_results = []
    for config in strategy_configs:
        result = run_config_simulation(config, df)
        all_results.append(result)
    leaderboard = pd.DataFrame(all_results)
    leaderboard.sort_values(by="net_return_pct", ascending=False, inplace=True)
    leaderboard.to_csv(output_path, index=False)
    print(f"Optimization complete. Results saved to {output_path}")
    return leaderboard

if __name__ == "__main__":
    run_optimizer()
