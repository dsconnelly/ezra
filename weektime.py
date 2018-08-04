"""This file defines the weektime module, which is a pared-down date/time
module designed to be used for representing the date/time information pertinent
to college course scheduling."""

class WeekTime(object):
    """This class is a date/time data structure that knows about no duration of
    time longer than a week. It ignores the year and the month and the day of
    the month."""
    def __init__(self, day, hour, minute):
        """Initializes the WeekTime object. The parameters are:
            day : must be an integer in [1..7] inclusive. 1 is Monday.
                Alternatively, can be None, which indicates a time independent
                of day of the week.
            hour : must be an integer in [0..23] inclusive.
            minute : must be an integer in [0..59] inclusive."""
        self.day = day
        self.hour = hour
        self.minute = minute

    # We define getters and setters to handle errors.

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, d):
        if type(d) is not int and d is not None:
            raise ValueError('Day must be an integer; got ' + str(d))
        try:
            if d < 1 or d > 7:
                raise ValueError('Day value must be in [1..7]; got ' + str(d))
        except TypeError:
            pass
        self._day = d

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

    # Here are some useful methods.

    def __repr__(self):
        return 'WeekTime(day=%s, hour=%s, minute=%s)' % (
            self.day, self.hour, self.minute)

    def __eq__(self, other):
        return (self.day == other.day
            and self.hour == other.hour
            and self.minute == other.minute)

    def __lt__(self, other):
        """Defines ordering on WeekTimes. Ordering is done by ordering in the
        week, where Monday morning is the beginning and Sunday night the end."""
        if self.day != other.day:
            return self.day < other.day
        if self.hour != other.hour:
            return self.hour < other.hour
        if self.minute != other.minute:
            return self.minute < other.minute
        return False

    def __le__(self, other):
        return self < other or self == other

def parse_time(s):
    """Returns a WeekTime object, given a string like '08:00AM'. Sets the
    result to have None day."""
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
    return WeekTime(None, hour, minute)
