import pytest
import sys
import os

# Add the parent directory to the system path so Python can find logic_utils.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic_utils import check_guess, parse_guess, get_temperature_hint

# --- Challenge 1: Advanced Edge Case Testing ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_parse_guess_valid_integer():
    ok, val, err = parse_guess("42")
    assert ok is True
    assert val == 42

def test_parse_guess_invalid_text():
    ok, val, err = parse_guess("apple")
    assert ok is False
    assert val is None

# EDGE CASE: Decimals should be gracefully rejected, not silently truncated
def test_parse_guess_decimal_edge_case():
    ok, val, err = parse_guess("42.5")
    assert ok is False
    assert err == "Please enter a whole number, not a decimal."

# EDGE CASE: Extremely large numbers
def test_check_guess_extreme_large():
    outcome, _ = check_guess(999999999999, 50)
    assert outcome == "Too High"

# EDGE CASE: Negative numbers
def test_check_guess_negative_edge_case():
    outcome, _ = check_guess(-100, 50)
    assert outcome == "Too Low"

# EDGE CASE: Empty inputs
def test_parse_guess_empty_string():
    ok, val, err = parse_guess("")
    assert ok is False
    assert err == "Enter a guess."

def test_temperature_hint():
    assert get_temperature_hint(50, 50) == "🎯"
    assert "BOILING" in get_temperature_hint(52, 50)
    assert "HOT" in get_temperature_hint(58, 50)
    assert "COLD" in get_temperature_hint(10, 50)