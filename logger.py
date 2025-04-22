import csv
import os

def log_trade(decision, balances, filepath='trades.csv'):
    file_exists = os.path.exists(filepath)
    with open(filepath, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['time', 'signal', 'reason', 'btc_balance', 'usd_balance'])
        writer.writerow([
            decision['time'],
            decision['signal'],
            decision['reason'],
            balances.get('BTC', '0'),
            balances.get('USD', '0')
        ])
