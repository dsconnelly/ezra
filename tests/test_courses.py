"""Tests for the courses module."""
import pytest
import apicode.courses as courses
import apicode.classtime as ct

# Tests for the Section class.
def test_section_int():
    d1 = ct.DayTime(9, 0)
    d2 = ct.DayTime(9, 50)
    s = courses.Section('LEC', 'John Doe', 'MWF', d1, d2)

    assert 'LEC' == s.kind
    assert 'John Doe' == s.instructor
    assert ['M', 'W', 'F'] == s.days
    assert d1 == s.start
    assert d2 == s.end

def test_parse_days():
    assert ['M', 'Su'] == courses.Section.parse_days('MSu')

def test_section_repr():
    d1 = ct.DayTime(9, 0)
    d2 = ct.DayTime(9, 50)
    s = courses.Section('LEC', 'John Doe', 'MWF', d1, d2)
    assert s == eval('courses.' + s.__repr__())

def test_section_as_json():
    d1 = ct.DayTime(9, 0)
    d2 = ct.DayTime(9, 50)
    s = courses.Section('LEC', 'John Doe', 'MWF', d1, d2)

    start_row = 1 + ((d1.hour - 8) * 12) + (d1.minute / 5)
    end_row = 1 + ((d2.hour - 8) * 12) + (d2.minute / 5)

    assert (s.as_json() == {
        'kind' : 'LEC',
        'instructor' : 'John Doe',
        'ref' : 'MWF 09:00 - 09:50',
        'day_idxs' : [1, 3, 5],
        'start_row' : start_row,
        'end_row' : end_row
    })

# Tests for the Course class.
def test_course_init():
    d1 = ct.DayTime(9, 0)
    d2 = ct.DayTime(9, 50)
    s = courses.Section('LEC', 'John Doe', 'MWF', d1, d2)
    c1 = courses.Course('Mathematics', 'MATH', 4130, 'Analysis', ['LEC'], [s])
    c2 = courses.Course('Mathematics', 'MATH', '4130', 'Analysis', ['LEC'], [s])

    assert c1 == c2
    assert (c1.as_json() == {
        'department' : 'Mathematics',
        'dept_short' : 'MATH',
        'number' : '4130',
        'title' : 'Analysis',
        'required' : ['LEC'],
        'sections' : [s.as_json()]
    })
