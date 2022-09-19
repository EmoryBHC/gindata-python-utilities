"""Tests for the ehashshift utility package"""
from ehashshift import (
    is_nan,
    date_shift,
)

def test_custom_isnan():
    """Confirm nan check returns expected values"""
    assert is_nan(float('nan'))
    assert is_nan(1) == False

def test_dateshift_when_given_nan():
    """Confirm function returns None when given a NaN value and seed"""
    result = date_shift(float('nan'),'123456789')
    assert result is None
