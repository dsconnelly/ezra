"""Tests for the apiquery module."""
import pytest
import apicode.query as query

# Tests for the Query class.
def test_init():
    q = query.Query()
    assert 'Mathematics' == q.department_keys['MATH']
    assert 'English' == q.department_keys['ENGL']

def test_get_course_by_dept_and_number():
    q = query.Query()
    c = q.get_course_by_dept_and_number('EAS', '3050')

    assert 'Climate Dynamics' == c.title
    assert ['LEC'] == c.required
    assert 1 == len(c.sections)
