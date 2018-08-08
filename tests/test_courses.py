"""Tests for the courses module."""
import unittest
import apicode.courses as courses
import apicode.weektime as wt

class MeetingTest(unittest.TestCase):
    """Tests for the MeetingGroup and Meeting classes, since the latter is
    created exclusively by the former."""
    def test_init(self):
        ws = wt.WeekTime(None, 8, 0)
        we = wt.WeekTime(None, 9, 0)
        mg = courses.MeetingGroup('LEC', 'John Doe', 'MWSu', ws, we, None)

        self.assertEqual(3, len(mg.meetings))
        self.assertEqual(1, mg.meetings[0].start.day)
        self.assertEqual(3, mg.meetings[1].start.day)
        self.assertEqual(7, mg.meetings[2].start.day)

    def test_parse_day_string(self):
        self.assertEqual(['M', 'W', 'F'],
            courses.MeetingGroup.parse_day_string('MWF'))
        self.assertEqual(['T', 'R', 'Su'],
            courses.MeetingGroup.parse_day_string('TRSu'))

    def test_meeting_order(self):
        ws = wt.WeekTime(None, 8, 0)
        we = wt.WeekTime(None, 9, 0)
        mg = courses.MeetingGroup('LEC', 'John Doe', 'MSu', ws, we, None)
        self.assertTrue(mg.meetings[0] < mg.meetings[1])

class CourseTest(unittest.TestCase):
    """Tests for the Course class."""
    def test_init(self):
        ws = wt.WeekTime(None, 8, 0)
        we = wt.WeekTime(None, 9, 0)
        mg = courses.MeetingGroup('LEC', 'John Doe', 'MWF', ws, we, None)

        c1 = courses.Course('Mathematics', 'MATH', 4130, 'Analysis',
            ['LEC'], [mg])
        c2 = courses.Course('Mathematics', 'MATH', '4130', 'Analysis',
            ['LEC'], [mg])
        self.assertEqual(4130, c1.number)
        self.assertEqual(4130, c2.number)

if __name__ == '__main__':
    unittest.main()
