"""Describes class for holding course information, like title, department,
professor, and meeting times, though meeting times will probably eventually
be refactored into another file."""

import apicode.classtime as ct

class Course(object):
    """A Course object represents an entire university course."""
    def __init__(self, department, dept_short, number, title, required,
        sections):
        """Initializes the Course object. The parameters are
            department : a string, like 'Mathematics'.
            dept_short : a string, like 'MATH'.
            number : an int or the corresponding string, like 4130 or '4130'.
            title : a string, like 'Analysis I'.
            required : a list of strings like 'LEC' and 'DIS'. Elements are
                required to be unique.
            sections : a list of Section objects.
        We also perform the appropriate checks on arguments to ensure they are
        what they are supposed to be."""
        if type(department) is not str:
            raise ValueError('Department must be a string; got '
                + str(department))
        self.department = department

        if type(dept_short) is not str:
            raise ValueError('Department short name must be a string; got '
                + str(dept_short))
        self.dept_short = dept_short

        try:
            self.number = str(int(number))
        except ValueError:
            raise ValueError('Course number must be castable as int; got '
                + str(number))

        if type(title) is not str:
            raise ValueError('Course title must be a string; got ' + str(title))
        self.title = title

        if type(required) is not list:
            raise ValueError('Course requirements must be a list')
        if sorted(required) != sorted(list(set(required))):
            raise ValueError('Course requirements must be unique')
        self.required = required

        if type(sections) is not list:
            raise ValueError('Course must be passed a list of Sections')
        if len(sections) == 0:
            raise ValueError('Course has no sections')
        for s in sections:
            if type(s) is not Section:
                raise ValueError('Course must be passed a list of Sections')
        self.sections = sections

    def as_json(self):
        """Returns a dictionary for later conversion to JSON. Note that we do
        not actually convert to JSON but rather return a dictionary."""
        return {
            'department' : self.department,
            'dept_short' : self.dept_short,
            'number' : self.number,
            'title' : self.title,
            'required' : self.required,
            'sections' : [s.as_json() for s in self.sections]
        }

    def __repr__(self):
        return ('Course(department=\'%s\', dept_short=\'%s\', number=%s, '
            + 'title=\'%s\', required=\'%s\')') % (self.department,
            self.dept_short, self.number, self.title, self.required)

    def __eq__(self, other):
        return (self.department == other.department
            and self.dept_short == other.dept_short
            and self.number == other.number
            and self.title == other.title
            and self.required == other.required)

class Section(object):
    """A Section refers to a lecture or discussion or so on, which may
    meet several times throughout the week."""
    allowed_kinds = ['LEC', 'DIS', 'LAB', 'TA', 'SEM', 'STU']
    allowed_days = ['M', 'T', 'W', 'R', 'F', 'S', 'Su']

    def __init__(self, kind, instructor, days, start, end):
        """Initializes the Section. The parameters are:
            kind : a string like 'LEC' or 'DIS'.
            instructor a string, the name of the instructor.
            days : a string like 'MWF'.
            start : a ct.DayTime object holding the start time.
            end : a ct.DayTime object holding the end time.
        At least for now, we do not do much input validation on these arguments,
        since this function will be called by apiquery and not the user."""
        if kind not in self.allowed_kinds:
            raise ValueError('Invalid Section kind: %s' % kind)
        if type(instructor) is not str:
            raise ValueError('Section instructor must be a string')
        if start >= end:
            raise ValueError('Section must start before it ends')

        self.kind = kind
        self.instructor = instructor

        self.days = self.parse_days(days)
        for d in self.days:
            if d not in self.allowed_days:
                raise ValueError('Unknown day code: %s') % d

        self.start = start
        self.end = end
        self.start_row, self.end_row = self.row_bounds(self.start, self.end)

    def as_json(self):
        """Returns a dictionary of useful values to be converted to JSON. Note
        that it is a dictionary that is returned, not an actual JSON string;
        we are just returning a dictionary that will be useful as JSON later."""
        return {
            'kind' : self.kind,
            'instructor' : self.instructor,
            'ref' : (''.join(self.days) + ' ' + self.start.as_tod_string()
                + ' - ' + self.end.as_tod_string()),
            'day_idxs' : [(self.allowed_days.index(d) + 1) for d in self.days],
            'start_row' : self.start_row,
            'end_row' : self.end_row
        }

    def __repr__(self):
        return ('Section(kind=\'%s\', instructor=\'%s\', days=\'%s\', '
            + 'start=ct.%s, end=ct.%s)') % (
                self.kind,
                self.instructor,
                ''.join(self.days),
                self.start,
                self.end
            )

    def __eq__(self, other):
        return (self.kind == other.kind
            and self.instructor == other.instructor
            and sorted(self.days) == sorted(other.days)
            and self.start == other.start
            and self.end == other.end)

    @staticmethod
    def parse_days(s):
        """Given a string like 'MWF', returns an array of the day codes. Needed
        because the Sunday code is 'Su', which is two characters."""
        output = []
        for c in s:
            if c == 'u':
                output[-1] += 'u'
            else:
                output.append(c)
        return output

    @staticmethod
    def row_bounds(start, end):
        """Computes and returns the start and end rows to be used, as a tuple.
        The first item is the first row to use, and the second item is the first
        row not to use."""
        start_row = 1 + ((start.hour - 8) * 12) + (start.minute / 5)
        end_row = 1 + ((end.hour - 8) * 12) + (end.minute / 5)
        return(start_row, end_row)
