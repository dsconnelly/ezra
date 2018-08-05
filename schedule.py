"""Defines a Schedule class that holds a variety of Course objects."""

import apiquery
import courses

class OverlapError(Exception):
    pass

class Schedule(object):
    """Represents a course schedule for a semester."""
    def __init__(self, roster='FA18'):
        self.query = apiquery.Query(roster)
        self.courses = []

    def no_conflicts(self):
        """Returns a boolean indicating whether or not the active meetings of
        the courses in the schedule have no conflicts."""
        for c1 in self.courses:
            for m1 in c1.all_active_meetings():
                for c2 in self.courses:
                    if c1 == c2:
                        continue
                    for m2 in c2.all_active_meetings():
                        if m1.overlap(m2):
                            return False
        return True

    def add_course_by_dept_and_number(self, dept_short, number):
        """Looks up a course by department abbreviation and number."""
        self.courses.append(self.query.get_course_by_dept_and_number(dept_short,
            number))

    def weekly_print(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday']
        schedule_by_day = {i : [] for i in range(1, 8)}

        for course in self.courses:
            for meeting in course.all_active_meetings():
                schedule_by_day[meeting.start.day].append(meeting)

        for i in range(1, 8):
            schedule_by_day[i].sort()

        for i in range(1, 8):
            print(days[i - 1].upper())
            for m in schedule_by_day[i]:
                mg = m.meeting_group
                c = mg.course
                print('%s %s %s: %s - %s' % (c.dept_short, str(c.number),
                    mg.kind, m.start.as_tod_string(), m.end.as_tod_string()))

if __name__ == '__main__':
    s = Schedule()
    s.add_course_by_dept_and_number('MATH', 4330)
    s.add_course_by_dept_and_number('CS', 4780)
    s.weekly_print()
