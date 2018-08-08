"""Tests for the apiquery module."""
import unittest
import apicode.apiquery as aq

class QueryTest(unittest.TestCase):
    """Tests for the Query class."""
    def test_init(self):
        q = aq.Query()
        self.assertEqual('Mathematics', q.department_keys['MATH'])
        self.assertEqual('English', q.department_keys['ENGL'])

    def test_get_course_by_dept_and_number(self):
        q = aq.Query()
        c = q.get_course_by_dept_and_number('EAS', 3050)

        self.assertEqual('Climate Dynamics', c.title)
        self.assertEqual(['LEC'], c.required)
        self.assertEqual(1, len(c.meeting_groups))
        self.assertEqual(3, len(c.meeting_groups[0].meetings))

if __name__ == '__main__':
    unittest.main()
