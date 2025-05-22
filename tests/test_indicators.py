import unittest
import sys
import pandas as pd
import numpy as np

# Add the parent directory to the sys.path to allow imports from the root directory
sys.path.append('..')

from indicators import add_indicators

class TestIndicators(unittest.TestCase):
    def setUp(self):
        """Set up a sample DataFrame for testing."""
        # Create a DataFrame with enough data for indicators to be calculated
        # Using a simple linear series for 'close' prices for predictability if needed
        close_prices = np.linspace(100, 150, 50) 
        self.df_sample = pd.DataFrame({'close': close_prices})
        
        # Create an empty DataFrame for testing empty input handling
        self.df_empty = pd.DataFrame({'close': []})

        # Create a DataFrame with insufficient data for some indicators
        close_prices_short = np.linspace(100, 110, 10)
        self.df_insufficient = pd.DataFrame({'close': close_prices_short})

    def test_add_indicators_columns_exist(self):
        """Test that all expected indicator columns are added."""
        df_processed = add_indicators(self.df_sample.copy()) # Use a copy to avoid modifying the original sample
        expected_columns = ['rsi', 'macd', 'macds', 'macdh', 'ema_12', 'ema_26']
        for col in expected_columns:
            self.assertIn(col, df_processed.columns)

    def test_add_indicators_return_type(self):
        """Test that the function returns a Pandas DataFrame."""
        df_processed = add_indicators(self.df_sample.copy())
        self.assertIsInstance(df_processed, pd.DataFrame)

    def test_add_indicators_output_not_empty(self):
        """Ensure the returned DataFrame is not empty for valid input."""
        df_processed = add_indicators(self.df_sample.copy())
        self.assertFalse(df_processed.empty)

    def test_add_indicators_data_types(self):
        """Check that indicator columns are of numeric type (float)."""
        df_processed = add_indicators(self.df_sample.copy())
        indicator_columns = ['rsi', 'macd', 'macds', 'macdh', 'ema_12', 'ema_26']
        for col in indicator_columns:
            # pandas-ta can sometimes produce all NaNs if data is too short,
            # which can lead to dtype object. So we check for float64 or that all values are NaN.
            if df_processed[col].notna().any(): # If there's at least one non-NaN value
                self.assertTrue(pd.api.types.is_float_dtype(df_processed[col]), f"Column {col} is not float type.")
            else: # If all are NaN, the dtype might be object, but it's acceptable.
                self.assertTrue(df_processed[col].isna().all(), f"Column {col} has mixed NaN/non-NaN with non-float type.")


    def test_add_indicators_handles_empty_input(self):
        """Test behavior with an empty DataFrame."""
        df_processed = add_indicators(self.df_empty.copy())
        self.assertIsInstance(df_processed, pd.DataFrame)
        # Depending on pandas-ta behavior, it might add columns of NaNs or keep it empty.
        # Let's check that it either is empty or has the expected columns (filled with NaNs).
        if not df_processed.empty:
            expected_columns = ['rsi', 'macd', 'macds', 'macdh', 'ema_12', 'ema_26']
            for col in expected_columns:
                self.assertIn(col, df_processed.columns)
            self.assertTrue(df_processed[expected_columns].isna().all().all(), "Expected all NaNs for empty input if columns are added.")
        else:
            self.assertTrue(df_processed.empty)


    def test_add_indicators_handles_insufficient_data(self):
        """Test with insufficient data, expecting NaNs but no errors."""
        df_processed = add_indicators(self.df_insufficient.copy())
        self.assertIsInstance(df_processed, pd.DataFrame)
        indicator_columns = ['rsi', 'macd', 'macds', 'macdh', 'ema_12', 'ema_26']
        for col in indicator_columns:
            self.assertIn(col, df_processed.columns)
        # With insufficient data, pandas-ta typically fills with NaNs.
        self.assertTrue(df_processed[indicator_columns].isna().all().all(), 
                        "Expected all indicator values to be NaN for insufficient data.")

    def test_add_indicators_string_index_logic(self):
        """Verify that the output DataFrame's index is of string type."""
        df_processed = add_indicators(self.df_sample.copy())
        self.assertTrue(all(isinstance(idx, str) for idx in df_processed.index), "Index is not of string type.")
        self.assertEqual(len(df_processed.index), len(self.df_sample), "Index length changed unexpectedly.")

    def test_some_non_nan_values_for_sufficient_data(self):
        """Check for some non-NaN values with sufficient data after warm-up."""
        df_large_enough = pd.DataFrame({'close': np.random.rand(100) * 100 + 50}) # 100 data points
        df_processed = add_indicators(df_large_enough)
        indicator_columns = ['rsi', 'macd', 'macds', 'macdh', 'ema_12', 'ema_26']
        
        # Check that after a certain period (e.g., last half of data), not all values are NaN
        # This accounts for initial NaN values due to indicator calculation windows
        check_from_row = len(df_processed) // 2 
        
        for col in indicator_columns:
            self.assertTrue(df_processed[col][check_from_row:].notna().any(),
                            f"Column {col} has all NaN values after warm-up period for sufficient data.")


if __name__ == '__main__':
    unittest.main()
