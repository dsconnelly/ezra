"""This file defines the classtime module, which is a pared-down date/time
module designed to be used for representing the date/time information pertinent
to college course scheduling."""

class DayTime(object):
    """The DayTime class is the parent class of WeekTime. Sometimes we don't
    care about the day of the week, and having a parent class with no day
    attribute is more elegant than having a meaningless day attribute that has
    to be set to None."""
    def __init__(self, hour, minute):
        """Initializes the DayTime object. The parameters are:
            hour : must be an integer in [0..23] inclusive.
            minute : must be an integer in [0..59] inclusive."""
        self.hour = hour
        self.minute = minute

    # We define getters and setters to handle invalid times.

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, h):
        if type(h) is not int:
            raise ValueError('Hour must be an integer; got ' + str(h))
        if h < 0 or h > 23:
            raise ValueError('Hour value must be in [0..23]; got ' + str(h))
        self._hour = h

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, m):
        if type(m) is not int:
            raise ValueError('Minute must be an integer; got ' + str(m))
        if m < 0 or m > 59:
            raise ValueError('Minute value must be in [0..59]; got ' + str(m))
        self._minute = m

    def as_tod_string(self):
        """Returns a string of the form '08:00'."""
        hour = str(self.hour)
        if len(hour) == 1:
            hour = '0' + hour
        minute = str(self.minute)
        if len(minute) == 1:
            minute = '0' + minute
        return '%s:%s' % (hour, minute)

    # Some class methods.

    def __repr__(self):
        return 'DayTime(hour=%s, minute=%s)' % (self.hour, self.minute)

    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute

    def __lt__(self, other):
        if self.hour != other.hour:
            return self.hour < other.hour
        if self.minute != other.minute:
            return self.minute < other.minute
        return False

    def __le__(self, other):
        return self < other or self == other

    @staticmethod
    def parse_time_string(s):
        """Returns a DayTime object, given a string like '08:00AM'."""
        if s == '':
            raise ValueError('Time string cannot be empty')
        hour = int(s[:2])
        if s[5:] == 'PM':
            if hour != 12:
                hour += 12
        else:
            if hour == 12:
                hour = 0
        minute = int(s[3:5])
        return DayTime(hour, minute)

class WeekTime(DayTime):
    """WeekTime objects are like DayTime objects, but they also store a day
    attribute corresponding to a day of the week."""
    def __init__(self, day, hour, minute):
        """Initializes the WeekTime object. The parameters are:
            day : must be an integer in [1..7] inclusive. 1 is Monday.
            hour : must be an integer in [0..23] inclusive.
            minute : must be an integer in [0..59] inclusive."""
        super().__init__(hour, minute)
        self.day = day

    # We define getters and setters to handle errors.

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, d):
        if type(d) is not int:
            raise ValueError('Day must be an integer; got ' + str(d))
        if d < 1 or d > 7:
            raise ValueError('Day value must be in [0..59]; got ' + str(d))
        self._day = d

    # Here are some useful methods.

    def __repr__(self):
        return 'WeekTime(day=%d, hour=%d, minute=%d)' % (
            self.day, self.hour, self.minute)

    def __eq__(self, other):
        return super().__eq__(other) and self.day == other.day

    def __lt__(self, other):
        if self.day != other.day:
            return self.day < other.day
        return super().__lt__(other)
