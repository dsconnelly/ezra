"""Describes class for holding course information, like title, department,
professor, and meeting times, though meeting times will probably eventually
be refactored into another file."""

class Course(object):
    """Large-scale object for an entire course."""
    def __init__(self, department, dept_short, number, title, professor):
        """Initializes the Course object. Course attributes are set as
        read-only. The parameters are
            department : a string, like 'Earth and Atmospheric Sciences'.
            dept_short : a string, like 'EAS'.
            number : an integer, like 3420.
            title : a string, like 'Climate Dynamics'.
            professor : a string, like 'Natalie Mahowald'."""
        if type(department) is not str:
            raise ValueError('Department must be a string; got '
                + str(department))
        self._department = department

        if type(dept_short) is not str:
            raise ValueError('Department short name must be a string; got '
                + str(dept_short))
        self._dept_short = dept_short

        if type(number) is not int:
            raise ValueError('Course number must be a string; got '
                + str(number))
        self._number = number

        if type(title) is not str:
            raise ValueError('Course title must be a string; got ' + str(title))
        self._title = title

        if type(professor) is not str:
            raise ValueError('Professor must be a string; got '
                + str(professor))
        self._professor = professor

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
    def professor(self):
        return self._professor

    def __repr__(self):
        return ('Course(department=\'%s\', dept_short=\'%s\', number=%s, '
            + 'title=\'%s\', professor=\'%s\')') % (self.department, self.dept_short,
            self.number, self.title, self.professor)

    def __eq__(self, other):
        return (self.department == other.department
            and self.dept_short == other.dept_short
            and self.number == other.number
            and self.title == other.title
            and self.professor == other.professor))
