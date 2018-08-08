"""Tests for the weektime module."""
import pytest
import apicode.classtime as ct

def test_daytime_init():
    d = ct.DayTime(18, 30)
    assert 18 == d.hour
    assert 30 == d.minute

def test_weektime_init():
    w = ct.WeekTime(3, 18, 30)
    assert 3 == w.day
    assert 18 == w.hour
    assert 30 == w.minute

def test_as_tod_string():
    d = ct.DayTime(18, 30)
    assert '18:30' == d.as_tod_string()

    d = ct.DayTime(3, 5)
    assert '03:05' == d.as_tod_string()

    w = ct.WeekTime(3, 18, 30)
    assert '18:30' == w.as_tod_string()

def test_init_bad_vals():
    with pytest.raises(ValueError):
        ct.WeekTime(10, 3, 15)
    with pytest.raises(ValueError):
        ct.WeekTime(1, 24, 15)
    with pytest.raises(ValueError):
        ct.WeekTime(1, 3, 60)

def test_repr():
    d = ct.DayTime(18, 29)
    assert d == eval('ct.' + d.__repr__())

    w = ct.WeekTime(2, 18, 29)
    assert w == eval('ct.' + w.__repr__())

def test_order():
    d1 = ct.DayTime(3, 0)
    d2 = ct.DayTime(3, 15)
    assert d1 < d2

    d1 = ct.DayTime(1, 15)
    d2 = ct.DayTime(2, 15)
    assert d1 < d2

    w1 = ct.WeekTime(1, 3, 15)
    w2 = ct.WeekTime(2, 3, 15)
    assert w1 < w2

def test_parse_time():
    d = ct.DayTime(7, 55)
    assert d == ct.DayTime.parse_time_string('07:55AM')

    d = ct.DayTime(17, 15)
    assert d == ct.DayTime.parse_time_string('05:15PM')
