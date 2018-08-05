"""Describes class for holding course information, like title, department,
professor, and meeting times, though meeting times will probably eventually
be refactored into another file."""

import weektime as wt

class Course(object):
    """Large-scale object for an entire course."""
    def __init__(self, department, dept_short, number, title, required,
        meeting_groups):
        """Initializes the Course object. Course attributes are set as
        read-only. The parameters are
            department : a string, like 'Earth and Atmospheric Sciences'.
            dept_short : a string, like 'EAS'.
            number : an integer, like 3420.
            title : a string, like 'Climate Dynamics'.
            required : a set of strings like 'LEC' and 'LAB'.
            meeting_groups : a list of MeetingGroup objects."""
        if type(department) is not str:
            raise ValueError('Department must be a string; got '
                + str(department))
        self._department = department

        if type(dept_short) is not str:
            raise ValueError('Department short name must be a string; got '
                + str(dept_short))
        self._dept_short = dept_short

        if type(number) is not int:
            raise ValueError('Course number must be an int; got '
                + str(number))
        self._number = number

        if type(title) is not str:
            raise ValueError('Course title must be a string; got ' + str(title))
        self._title = title

        if type(required) is not set:
            raise ValueError('Course requirements must be a set')
        self._required = required

        self._meeting_groups = meeting_groups
        for mg in self.meeting_groups:
            mg.course = self

        # We set a default activation.
        for kind in self.required:
            found = False
            for mg in self.meeting_groups:
                if mg.kind == kind:
                    mg.active = True
                    found = True
            if found:
                continue

    @property
    def department(self):
        return self._department

    @property
    def dept_short(self):
        return self._dept_short

    @property
    def number(self):
        return self._number

    @property
    def title(self):
        return self._title

    @property
    def required(self):
        return self._required

    @property
    def meeting_groups(self):
        return self._meeting_groups

    def __repr__(self):
        return ('Course(department=\'%s\', dept_short=\'%s\', number=%s, '
            + 'title=\'%s\')') % (self.department, self.dept_short,
            self.number, self.title)

    def __eq__(self, other):
        return (self.department == other.department
            and self.dept_short == other.dept_short
            and self.number == other.number
            and self.title == other.title)

    def all_active_meetings(self):
        """Returns a list of all meetings associated with this course that
        belong to an active MeetingGroup."""
        output = []
        for mg in self.meeting_groups:
            if mg.active:
                for m in mg.meetings:
                    output.append(m)
        return output

class MeetingGroup(object):
    """A MeetingGroup refers to a lecture or discussion or so on, which may
    meet several times throughout the week."""
    allowed_kinds = ['LEC', 'DIS', 'LAB', 'TA', 'SEM']
    allowed_days = 'MTWRF'

    def __init__(self, kind, instructor, days, start, end, course,
        active=False):
        """Initializes the Meeting. The parameters are:
            kind : a string like 'LEC' or 'DIS'.
            instructor : a string, the name of the instructor.
            days : a string like 'MWF'.
            start : a WeekTime object holding the start time.
            end : a WeekTime object holding the end time.
            active : a boolean value indicating whether the MeetingGroup has
                been selected to be enrolled in.
            course : the course to which this MeetingGroup belongs.
        Though it does not, strictly speaking, matter, the start and end
        WeekTimes should have day values of None, for good practice."""
        if kind not in self.allowed_kinds:
            raise ValueError('Invalid MeetingGroup type: %s' % kind)
        if type(instructor) is not str:
            raise ValueError('MeetingGroup professor must be a string')
        if start >= end:
            raise ValueError('Meeting must start before it ends')

        self.kind = kind
        self.instructor = instructor

        self.meetings = []
        for d in days:
            try:
                d_idx = self.allowed_days.find(d) + 1
            except ValueError:
                raise ValueError('Unknown day code: %s' % d)
            m_start = wt.WeekTime(d_idx, start.hour, start.minute)
            m_end = wt.WeekTime(d_idx, end.hour, end.minute)
            self.meetings.append(Meeting(m_start, m_end, self))
        self.active = active

class Meeting(object):
    """A Meeting refers to a single event during the week."""
    def __init__(self, start, end, mg):
        """Since for now only MeetingGroup will call this, we will assume
        that the start and end times are acceptable. Parameter mg is a
        MeetingGroup object to which this meeting belongs."""
        self.start = start
        self.end = end
        self.meeting_group = mg

    def overlap(self, other):
        """Determines if two Meeting objects overlap in time."""
        # TODO: figure  out edge cases involving equality.
        if self.start < other.start:
            return other.start < self.end
        return self.start < other.end

    def __lt__(self, other):
        """We define an order on Meeting objects based on start times.
        In practice, this should only be called on Meeting objects known not to
        overlap that occur on the same day."""
        return self.start < other.start

    def __le__(self, other):
        return self.start <= other.start
