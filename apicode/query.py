"""Various functions for querying the Cornell Scheduler API and returning
objects with class information as defined in the courses module."""

import requests
import apicode.courses as courses
import apicode.classtime as ct

class ClassNotFoundError(Exception):
    pass

class InvalidSearchError(Exception):
    pass

class Query(object):
    """Class for holding together various functions and variables related to
    API queries. Defined as a class to avoid true globals. We also pin a
    specific roster to each Query instance."""
    base_url = 'https://classes.cornell.edu/api/2.0/'

    def __init__(self, roster='FA18'):
        """Pulls the list of of department long names, useful later."""
        self.roster = roster

        response = requests.get(self.base_url
            + 'config/subjects.json?roster=%s' % self.roster).json()
        subjects = response['data']['subjects']

        self.dept_keys = {}
        for s in subjects:
            self.dept_keys[s['value']] = s['descrformal']

    def parse_course_json(self, json):
        """Given the full json dictionary for a given course, returns a Course
        object appropriately filled."""
        dept_short = json['subject']
        department = self.dept_keys[dept_short]
        number = json['catalogNbr']
        title = json ['titleLong']

        # Whether different enrollment patterns are truly divided into different
        # enrollGroups seems to vary widely by department and course. I would
        # just pull all the meetings from all enrollGroups, but the required
        # items could theoretically change between enrollGroups. I'm not sure
        # if that happens. We check for it here. TODO: figure this out.
        required = None
        for e in json['enrollGroups']:
            if required == None:
                required = e['componentsRequired']
            elif sorted(required) != sorted(e['componentsRequired']):
                raise RuntimeError('enrollGroups have different demands')
        if sorted(required) != sorted(list(set(required))):
            raise RuntimeError('API query yielded non-unique requirements')

        sections = []
        for eg in json['enrollGroups']:
            for cs in eg['classSections']:
                kind = cs['ssrComponent']

                for sec in cs['meetings']:
                    instructor = []
                    for i in sec['instructors']:
                        instructor.append(i['firstName'] + ' ' + i['lastName'])
                    instructor = ', '.join(instructor)

                    days = sec['pattern']

                    try:
                        start = ct.DayTime.parse_time_string(sec['timeStart'])
                        end = ct.DayTime.parse_time_string(sec['timeEnd'])
                    except ValueError:
                        continue

                    try:
                        sections.append(courses.Section(kind, instructor, days,
                            start, end))
                    except ValueError:
                        continue

        try:
            return courses.Course(department, dept_short, number, title,
                required, sections)
        except ValueError:
            return None

    def parse_search(self, s):
        """Given a string s entered by the user, tries to return a Course
        matching the search terms. First looks for full department names (since
        those are less likely to occur by chance in other queries) and then for
        department abbreviations. When multiple are found, takes the longest."""
        s_test = s.upper()
        abbrs = [x.upper() for x in list(self.dept_keys.keys())]
        longs = [x.upper() for x in list(self.dept_keys.values())]

        try:
            best_abbr = sorted([x for x in abbrs if x in s_test], key=len)[-1]
        except IndexError:
            best_abbr = ''
        try:
            best_long = sorted([x for x in longs if x in s_test], key=len)[-1]
        except IndexError:
            best_long = ''

        if best_long != '':
            idx = list(self.dept_keys.values()).index(best_long.title())
            dept_short = list(self.dept_keys.keys())[idx]
        elif best_abbr != '':
            dept_short = best_abbr
        else:
            raise InvalidSearchError('No department recognized: %s' % s)

        number = self.biggest_number_in_string(s)
        if number is None:
            raise InvalidSearchError('No number recognized: %s' % s)
        return self.get_course_by_dept_and_number(dept_short, number)

    def get_courses_by_dept_short(self, dept_short):
        """Given a department abbreviation (like 'EAS'), return a list of Course
        objects in the given roster and subject. Raise a ClassNotFoundError if
        no results are found."""
        try:
            department = self.dept_keys[dept_short]
        except KeyError:
            raise ValueError('%s is not a valid department' % dept_short)

        parameters = {'roster' : self.roster, 'subject' : dept_short}

        response = requests.get(self.base_url + 'search/classes.json',
            params=parameters)
        if response.status_code == 404:
            raise ClassNotFoundError('No %s classes found in roster %s'
                % (dept_short, roster))

        classes = response.json()['data']['classes']
        output = [self.parse_course_json(c) for c in classes]
        return [c for c in output if c is not None]

    def get_course_by_dept_and_number(self, dept_short, number):
        """Finds a specific course with a department abbreviation (like 'EAS')
        and a number. Raises a ClassNotFound error if no such class is found."""
        dept_courses = self.get_courses_by_dept_short(dept_short)
        for c in dept_courses:
            if int(c.number) == int(number):
                return c
        raise ClassNotFoundError('Could not find ' + dept_short + ' '
            + str(number))

    @staticmethod
    def biggest_number_in_string(s):
        """Given a string, finds the largest number present. Useful for trying
        to parse user searches."""
        numbers = []
        i = 0
        in_number = False
        for j, c in enumerate(s):
            if not in_number:
                if c.isdigit():
                    i = j
                    in_number = True
            else:
                if not c.isdigit():
                    numbers.append(int(s[i:j]))
                    in_number = False
        if in_number:
            numbers.append(int(s[i:]))
        try:
            return str(max(numbers))
        except ValueError:
            return None
