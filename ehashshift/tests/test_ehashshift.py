"""Tests for the ehashshift utility package"""
from ehashshift import (
    isNaN,
    date_shift,
)

def test_custom_isnan():
    """Confirm nan check returns expected values"""
    assert isNaN(float('nan'))
    assert isNaN(1) == False

def test_dateshift_when_given_nan():
    """Confirm function returns None when given a NaN value"""
    result = date_shift(float('nan'))
    assert result is None
