"""Tests for the courses module."""
import pytest
import apicode.courses as courses
import apicode.weektime as wt

# Tests for the MeetingGroup and Meeting classes, since the latter is created
# exclusively by the former.

def test_meeting_init():
    ws = wt.WeekTime(None, 8, 0)
    we = wt.WeekTime(None, 9, 0)
    mg = courses.MeetingGroup('LEC', 'John Doe', 'MWSu', ws, we, None)

    assert 3 == len(mg.meetings)
    assert 1 == mg.meetings[0].start.day
    assert 3 == mg.meetings[1].start.day
    assert 7 == mg.meetings[2].start.day

def test_parse_day_string():
    assert ['M', 'W', 'F'] == courses.MeetingGroup.parse_day_string('MWF')
    assert ['T', 'R', 'Su'] == courses.MeetingGroup.parse_day_string('TRSu')

def test_meeting_order():
    ws = wt.WeekTime(None, 8, 0)
    we = wt.WeekTime(None, 9, 0)
    mg = courses.MeetingGroup('LEC', 'John Doe', 'MSu', ws, we, None)
    assert mg.meetings[0] < mg.meetings[1]

# Tests for the Course class.
def test_course_init():
    ws = wt.WeekTime(None, 8, 0)
    we = wt.WeekTime(None, 9, 0)
    mg = courses.MeetingGroup('LEC', 'John Doe', 'MWF', ws, we, None)

    c1 = courses.Course('Mathematics', 'MATH', 4130, 'Analysis',
        ['LEC'], [mg])
    c2 = courses.Course('Mathematics', 'MATH', '4130', 'Analysis',
        ['LEC'], [mg])
    assert c1.number == c2.number
