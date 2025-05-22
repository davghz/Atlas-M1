import unittest
import sys

# Add the parent directory to the sys.path to allow imports from the root directory
sys.path.append('..')

from risk import calculate_position_size, check_max_exposure

class TestRisk(unittest.TestCase):
    def test_calculate_position_size_normal(self):
        # Test with typical values (e.g., usd_balance=10000, price=50000, risk_pct=0.02)
        # Expected: (10000 * 0.02) / 50000 = 0.004 BTC
        self.assertAlmostEqual(calculate_position_size(10000, 50000, 0.02), 0.004)

    def test_calculate_position_size_zero_price(self):
        # Test with price=0
        # Expected: 0 BTC
        self.assertAlmostEqual(calculate_position_size(10000, 0, 0.02), 0)

    def test_calculate_position_size_zero_balance(self):
        # Test with usd_balance=0
        # Expected: 0 BTC
        self.assertAlmostEqual(calculate_position_size(0, 50000, 0.02), 0)

    def test_calculate_position_size_different_risk_pct(self):
        # Test with a different risk_pct (e.g., 0.05)
        # Expected: (10000 * 0.05) / 50000 = 0.01 BTC
        self.assertAlmostEqual(calculate_position_size(10000, 50000, 0.05), 0.01)

    def test_calculate_position_size_rounding(self):
        # Ensure the output is rounded to 8 decimal places as specified in the function.
        # For example, if calculation is 0.123456789, it should be 0.12345679.
        self.assertAlmostEqual(calculate_position_size(1, 3, 1), 0.33333333) # 1/3
        self.assertAlmostEqual(calculate_position_size(123456789, 10000000000000000, 1), 0.00000001) # Test rounding up

    def test_check_max_exposure_within_limit(self):
        # Test with current_exposure < max_exposure_pct (e.g., 0.5 < 1.0)
        # Expected: True
        self.assertTrue(check_max_exposure(0.5, 1.0))

    def test_check_max_exposure_at_limit(self):
        # Test with current_exposure == max_exposure_pct (e.g., 1.0 == 1.0)
        # Expected: True
        self.assertTrue(check_max_exposure(1.0, 1.0))

    def test_check_max_exposure_over_limit(self):
        # Test with current_exposure > max_exposure_pct (e.g., 1.1 > 1.0)
        # Expected: False
        self.assertFalse(check_max_exposure(1.1, 1.0))

    def test_check_max_exposure_custom_max(self):
        # Test with a different max_exposure_pct (e.g., current_exposure=0.8, max_exposure_pct=0.7)
        # Expected: False
        self.assertFalse(check_max_exposure(0.8, 0.7))


if __name__ == '__main__':
    unittest.main()
