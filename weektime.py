"""This file defines the weektime module, which is a pared-down date/time
module designed to be used for representing the date/time information pertinent
to college course scheduling."""

class WeekTime(object):
    """This class is a date/time data structure that knows about no duration of
    time longer than a week. It ignores the year and the month and the day of
    the month."""

    DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
        'saturday', 'sunday']

    def __init__(self, day, hour, minute):
        """Initializes the WeekTime object. the parameters are:
            day - can be the name of a day, the three-letter abbreviation of a
                day, or the number of the day, where Monday is 1.
            hour - must be an integer in [0..23] inclusive.
            minute - must be an integer in [0..59] inclusive.
        This function assigns instance variable values."""
        self.day = day
        self.hour = hour
        self.minute = minute

    # The following blocks of code are getters and setters of the WeekTime's
    # three main instance variables.

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, d):
        if type(d) is int:
            if 1 <= d and d < 8:
                self._day = d
            else:
                raise ValueError('Day value out of bounds: ' + str(d))
        elif type(d) is str:
            if d.lower() in self.DAYS:
                self._day = self.DAYS.index(d.lower()) + 1
            elif d.lower() in [x[:3] for x in self.DAYS]:
                self._day = [x[:3] for x in self.DAYS].index(d.lower()) + 1
            else:
                raise ValueError('Invalid day string: ' + d)
        else:
            raise ValueError('Invalid day specified: ' + str(d))

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, h):
        if type(h) is int:
            if 0 <= h and h < 24:
                self._hour = h
            else:
                raise ValueError('Hour must be in [0..23] inclusive: ' + str(h))
        else:
            raise ValueError('Hour must be an integer: ' + str(h))

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, m):
        if type(m) is int:
            if 0 <= m and m < 60:
                self._minute = m
            else:
                raise ValueError('Minute must be in [0..59] inclusive: '
                    + str(m))
        else:
            raise ValueError('Minute must be an integer: ' + str(m))
