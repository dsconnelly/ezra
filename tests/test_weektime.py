"""Tests for the weektime module."""
import unittest
import apicode.weektime as wt

class WeekTimeTest(unittest.TestCase):
    """Tests for the WeekTime class."""
    def test_init(self):
        w = wt.WeekTime(2, 18, 29)
        self.assertEqual(2, w.day)
        self.assertEqual(18, w.hour)
        self.assertEqual(29, w.minute)

    def test_init_bad_vals(self):
        self.assertRaises(ValueError, wt.WeekTime, 10, 3, 15)
        self.assertRaises(ValueError, wt.WeekTime, 1, 24, 15)
        self.assertRaises(ValueError, wt.WeekTime, 1, 3, 60)

    def test_as_tod_string(self):
        w = wt.WeekTime(2, 18, 29)
        self.assertEqual('18:29', w.as_tod_string())
        w = wt.WeekTime(2, 3, 5)
        self.assertEqual('03:05', w.as_tod_string())

    def test_repr(self):
        w = wt.WeekTime(2, 18, 29)
        self.assertEqual(w, eval('wt.' + w.__repr__()))

    def test_order(self):
        w1 = wt.WeekTime(1, 3, 15)
        w2 = wt.WeekTime(2, 3, 15)
        self.assertTrue(w1 < w2)

        w1 = wt.WeekTime(1, 3, 15)
        w2 = wt.WeekTime(1, 4, 15)
        self.assertTrue(w1 < w2)

        w1 = wt.WeekTime(1, 3, 15)
        w2 = wt.WeekTime(1, 3, 16)
        self.assertTrue(w1 < w2)

    def test_parse_time(self):
        w = wt.WeekTime(None, 7, 55)
        self.assertEqual(w, wt.parse_time('07:55AM'))

        w = wt.WeekTime(None, 17, 15)
        self.assertEqual(w, wt.parse_time('05:15PM'))

if __name__ == '__main__':
    unittest.main()
