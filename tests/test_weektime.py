"""Tests for the weektime module."""
import pytest
import apicode.weektime as wt

def test_init():
    w = wt.WeekTime(2, 18, 29)
    assert 2 == w.day
    assert 18 == w.hour
    assert 29 == w.minute

def test_init_bad_vals():
    with pytest.raises(ValueError):
        wt.WeekTime(10, 3, 15)
    with pytest.raises(ValueError):
        wt.WeekTime(1, 24, 15)
    with pytest.raises(ValueError):
        wt.WeekTime(1, 3, 60)

def test_as_tod_string():
    w = wt.WeekTime(2, 18, 29)
    assert '18:29' == w.as_tod_string()

    w = wt.WeekTime(2, 3, 5)
    assert '03:05' == w.as_tod_string()

def test_repr():
    w = wt.WeekTime(2, 18, 29)
    assert w == eval('wt.' + w.__repr__())

def test_order():
    w1 = wt.WeekTime(1, 3, 15)
    w2 = wt.WeekTime(2, 3, 15)
    assert w1 < w2

    w1 = wt.WeekTime(1, 3, 15)
    w2 = wt.WeekTime(1, 4, 15)
    assert w1 < w2

    w1 = wt.WeekTime(1, 3, 15)
    w2 = wt.WeekTime(1, 3, 16)
    assert w1 < w2

def test_parse_time():
    w = wt.WeekTime(None, 7, 55)
    assert w == wt.parse_time('07:55AM')

    w = wt.WeekTime(None, 17, 15)
    assert w == wt.parse_time('05:15PM')
