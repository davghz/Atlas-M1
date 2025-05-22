import unittest
import sys
import pandas as pd
from datetime import datetime

# Add the parent directory to the sys.path to allow imports from the root directory
sys.path.append('..')

from strategy import decide_trade

class TestStrategy(unittest.TestCase):
    def _create_mock_row(self, rsi=None, macd=None, macds=None, close=100, timestamp=1678886400): # 2023-03-15 12:00:00 UTC
        return pd.Series({
            'rsi': rsi,
            'macd': macd,
            'macds': macds,
            'close': close,
            'timestamp': timestamp
        })

    def test_decide_trade_buy_signal(self):
        # RSI < rsi_buy (default 40) and MACD > MACDS
        row_data = self._create_mock_row(rsi=30, macd=0.5, macds=0.4)
        expected_time = datetime.utcfromtimestamp(row_data['timestamp']).strftime("%Y-%m-%d %H:%M")
        expected_decision = {"signal": "BUY", "reason": "RSI below 40 and MACD crossover", "time": expected_time}
        self.assertEqual(decide_trade(row_data), expected_decision)

    def test_decide_trade_sell_signal(self):
        # RSI > rsi_sell (default 60) and MACD < MACDS
        row_data = self._create_mock_row(rsi=70, macd=0.4, macds=0.5)
        expected_time = datetime.utcfromtimestamp(row_data['timestamp']).strftime("%Y-%m-%d %H:%M")
        expected_decision = {"signal": "SELL", "reason": "RSI above 60 and MACD crossdown", "time": expected_time}
        self.assertEqual(decide_trade(row_data), expected_decision)

    def test_decide_trade_hold_signal_no_clear_condition(self):
        # Neither buy nor sell criteria are met (e.g., RSI between thresholds)
        row_data = self._create_mock_row(rsi=50, macd=0.5, macds=0.4) # RSI is neutral, MACD would suggest buy
        expected_time = datetime.utcfromtimestamp(row_data['timestamp']).strftime("%Y-%m-%d %H:%M")
        expected_decision = {"signal": "HOLD", "reason": "No clear signal", "time": expected_time}
        self.assertEqual(decide_trade(row_data), expected_decision)

        row_data = self._create_mock_row(rsi=50, macd=0.4, macds=0.5) # RSI is neutral, MACD would suggest sell
        expected_decision = {"signal": "HOLD", "reason": "No clear signal", "time": expected_time}
        self.assertEqual(decide_trade(row_data), expected_decision)

    def test_decide_trade_hold_signal_missing_rsi(self):
        row_data = self._create_mock_row(rsi=None, macd=0.5, macds=0.4)
        expected_time = datetime.utcfromtimestamp(row_data['timestamp']).strftime("%Y-%m-%d %H:%M")
        expected_decision = {"signal": "HOLD", "reason": "Missing indicator data", "time": expected_time}
        self.assertEqual(decide_trade(row_data), expected_decision)

    def test_decide_trade_hold_signal_missing_macd(self):
        row_data = self._create_mock_row(rsi=30, macd=None, macds=0.4)
        expected_time = datetime.utcfromtimestamp(row_data['timestamp']).strftime("%Y-%m-%d %H:%M")
        expected_decision = {"signal": "HOLD", "reason": "Missing indicator data", "time": expected_time}
        self.assertEqual(decide_trade(row_data), expected_decision)

    def test_decide_trade_hold_signal_missing_macds(self):
        row_data = self._create_mock_row(rsi=30, macd=0.5, macds=None)
        expected_time = datetime.utcfromtimestamp(row_data['timestamp']).strftime("%Y-%m-%d %H:%M")
        expected_decision = {"signal": "HOLD", "reason": "Missing indicator data", "time": expected_time}
        self.assertEqual(decide_trade(row_data), expected_decision)

    def test_decide_trade_custom_rsi_thresholds(self):
        rsi_buy_custom = 30
        rsi_sell_custom = 70
        # Test BUY with custom threshold
        row_buy = self._create_mock_row(rsi=25, macd=0.5, macds=0.4)
        expected_time_buy = datetime.utcfromtimestamp(row_buy['timestamp']).strftime("%Y-%m-%d %H:%M")
        expected_decision_buy = {"signal": "BUY", "reason": f"RSI below {rsi_buy_custom} and MACD crossover", "time": expected_time_buy}
        self.assertEqual(decide_trade(row_buy, rsi_buy=rsi_buy_custom, rsi_sell=rsi_sell_custom), expected_decision_buy)

        # Test SELL with custom threshold
        row_sell = self._create_mock_row(rsi=75, macd=0.4, macds=0.5)
        expected_time_sell = datetime.utcfromtimestamp(row_sell['timestamp']).strftime("%Y-%m-%d %H:%M")
        expected_decision_sell = {"signal": "SELL", "reason": f"RSI above {rsi_sell_custom} and MACD crossdown", "time": expected_time_sell}
        self.assertEqual(decide_trade(row_sell, rsi_buy=rsi_buy_custom, rsi_sell=rsi_sell_custom), expected_decision_sell)

    def test_decide_trade_timestamp_formatting(self):
        input_timestamp = 1678886400 # This is 2023-03-15 12:00:00 UTC
        row_data = self._create_mock_row(rsi=30, macd=0.5, macds=0.4, timestamp=input_timestamp)
        decision = decide_trade(row_data)

        # Parse the time string from the decision back to a datetime object
        parsed_time_str = decision['time']
        parsed_datetime_obj = datetime.strptime(parsed_time_str, "%Y-%m-%d %H:%M")

        # Create the expected datetime object from the input timestamp
        expected_datetime_obj = datetime.utcfromtimestamp(input_timestamp)

        # Compare year, month, day, hour, minute
        self.assertEqual(parsed_datetime_obj.year, expected_datetime_obj.year)
        self.assertEqual(parsed_datetime_obj.month, expected_datetime_obj.month)
        self.assertEqual(parsed_datetime_obj.day, expected_datetime_obj.day)
        self.assertEqual(parsed_datetime_obj.hour, expected_datetime_obj.hour)
        self.assertEqual(parsed_datetime_obj.minute, expected_datetime_obj.minute)

    def test_decide_trade_invalid_timestamp(self):
        # Test with missing timestamp
        row_missing_ts = self._create_mock_row(rsi=30, macd=0.5, macds=0.4)
        row_missing_ts.pop('timestamp') # Remove timestamp
        decision_missing = decide_trade(row_missing_ts)
        self.assertEqual(decision_missing['time'], "1970-01-01 00:00") # Default time for missing/invalid ts

        # Test with None timestamp
        row_none_ts = self._create_mock_row(rsi=30, macd=0.5, macds=0.4, timestamp=None)
        decision_none = decide_trade(row_none_ts)
        self.assertEqual(decision_none['time'], "1970-01-01 00:00")

        # Test with string timestamp (invalid type for the processing in decide_trade)
        row_str_ts = self._create_mock_row(rsi=30, macd=0.5, macds=0.4, timestamp="not-a-timestamp")
        decision_str = decide_trade(row_str_ts)
        self.assertEqual(decision_str['time'], "1970-01-01 00:00")

if __name__ == '__main__':
    unittest.main()
