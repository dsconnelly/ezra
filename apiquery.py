"""Various functions for querying the Cornell Scheduler API and returning
objects with class information as defined in the courses module."""

import requests
import courses
import weektime as wt

class ClassNotFoundError(Exception):
    pass

class Query(object):
    """Class for holding together various functions and variables related to
    API queries. Defined as a class to avoid true globals. We also pin a
    specific roster to each Query instance."""
    base_url = 'https://classes.cornell.edu/api/2.0/'

    def __init__(self, roster='SP18'):
        """Pulls the list of of department long names, useful later."""
        self.roster = roster

        response = requests.get(self.base_url
            + 'config/subjects.json?roster=%s' % self.roster).json()
        subjects = response['data']['subjects']

        self.department_keys = {}
        for s in subjects:
            self.department_keys[s['value']] = s['descrformal']

    def parse_course_json(self, json):
        """Given the full json dictionary for a given course, returns a Course
        object appropriately filled."""
        dept_short = json['subject']
        department = self.department_keys[dept_short]
        number = int(json['catalogNbr'])
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
        required = set(required)

        meeting_groups = []
        for e in json['enrollGroups']:
            for cs in e['classSections']:
                kind = cs['ssrComponent']
                if kind == 'IND':
                    continue
                for mg in cs['meetings']:
                    instructor = []
                    for i in mg['instructors']:
                        instructor.append(i['firstName'] + i['lastName'])
                    instructor = ', '.join(instructor)
                    days = mg['pattern']
                    try:
                        start = wt.parse_time(mg['timeStart'])
                        end = wt.parse_time(mg['timeEnd'])
                    except ValueError:
                        continue
                    mg_instance = courses.MeetingGroup(kind, instructor, days,
                        start, end)
                    meeting_groups.append(mg_instance)
        if meeting_groups != []:
            return courses.Course(department, dept_short, number, title,
                required, meeting_groups)
        return None

    def get_courses_by_dept(self, dept_short):
        """Given a department abbreviation (like 'EAS'), return a list of Course
        objects in the given roster and subject. Raise a ClassNotFoundError if
        no results are found."""
        try:
            department = self.department_keys[dept_short]
        except KeyError:
            raise ValueError('%s is not a valid department' % dept_short)

        parameters = {'roster' : self.roster, 'subject' : dept_short}

        response = requests.get(self.base_url + 'search/classes.json',
            params=parameters)
        if response.status_code == 404:
            raise ClassNotFoundError('No %s classes found in roster %s'
                % (dept_short, roster))
        classes = response.json()['data']['classes']

        output = []
        for c in classes:
            course_inst = self.parse_course_json(c)
            if course_inst is not None:
                output.append(self.parse_course_json(c))
        return output

    def get_course_by_dept_and_number(self, dept_short, number):
        """Finds a specific course with a department abbreviation (like 'EAS')
        and a number. Raises a ClassNotFound error if no such class is found."""
        dept_courses = self.get_courses_by_dept(dept_short)
        for c in dept_courses:
            if c.number == number:
                return c
        raise ClassNotFoundError('Could not find ' + dept_short + ' '
            + str(number))

if __name__ == '__main__':
    q = Query()
    print(q.get_courses_by_dept('MATH'))
