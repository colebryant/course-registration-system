"""
Module: Repositories/Entities relating to People (Student & Instructor) Context
"""
from abc import ABC


class StudentLibrary:
    """Repository for students. Implemented as singleton"""
    __instance__ = None

    def __init__(self):
        if StudentLibrary.__instance__ is None:
            self.students = {}  # dict of Students: key = username, value =
            # Student
        else:
            raise Exception('Cannot create another StudentLibrary class')

    def retrieve_data(self, sql_retrieve):
        student_list = sql_retrieve.get_students()
        for s in student_list:
            current_student = Student(**s)
            self.add_student(s['username'], current_student)

    def add_student(self, username, student):
        self.students[username] = student

    def get_student(self, username):
        if username in self.students:
            return self.students[username]
        else:
            return None


class InstructorLibrary:
    """Repository for instructors. Implemented as singleton"""
    __instance__ = None

    def __init__(self):
        if InstructorLibrary.__instance__ is None:
            self.instructors = {}  # dict of Instructors: key = username, value
            # = Instructor
        else:
            raise Exception('Cannot create another InstructorLibrary class')

    def retrieve_data(self, sql_retrieve):
        instructor_list = sql_retrieve.get_instructors()
        for i in instructor_list:
            current_instructor = Instructor(**i)
            self.add_instructor(i['username'], current_instructor)

    def add_instructor(self, username, instructor):
        self.instructors[username] = instructor

    def get_instructor(self, username):
        if username in self.instructors:
            return self.instructors[username]
        else:
            return None


class Person(ABC):
    """Abstract base class for person entity in registration system"""

    def __init__(self, first_name, last_name, university_id, username,
                 department):
        self.first_name = first_name
        self.last_name = last_name
        self.university_id = university_id
        self.username = username
        self.department = department


class Student(Person):
    """Entity representing student in registration system"""

    def __init__(self, **kwargs):
        super().__init__(kwargs['first_name'], kwargs['last_name'],
                         kwargs['university_id'], kwargs['username'],
                         kwargs['department'])
        self.is_full_time = kwargs['is_full_time']
        self.major = kwargs['major']
        self.program = kwargs['program']
        self.schedule = StudentSchedule()

    @property
    def is_fully_registered(self):
        section_count = self.schedule.get_section_count()
        if self.is_full_time:
            if section_count >= 3:
                return True
            else:
                return False
        else:
            if section_count >= 2:
                return True
            else:
                return False

    def add_section(self, section):
        self.schedule.add_section(section)

    def add_lab(self, lab):
        self.schedule.add_lab(lab)

    def get_schedule(self):
        return self.schedule

    def view_grades(self):
        return self.schedule.view_grades(self.username, self.first_name,
                                        self.last_name)

    def view_schedule(self):
        return self.schedule.view_schedule(self.username, self.first_name,
                                          self.last_name)

    def __str__(self):
        if self.is_full_time:
            classification = 'Full-Time'
        else:
            classification = 'Part-Time'
        return f'Student({self.username}): {self.first_name} ' \
               f'{self.last_name}, {classification}, {self.program}'


class StudentSchedule:
    """Entity representing a student's schedule"""

    def __init__(self):
        self.sections = {}  # sections registered: key = course_name, value =
        # Section
        self.labs = {}  # labs registered: key = course_name, value = Lab

    def add_section(self, section):
        self.sections[section.course_name] = section

    def add_lab(self, lab):
        self.labs[lab.course_name] = lab

    def remove_section(self, course_name):
        del self.sections[course_name]

    def remove_lab(self, course_name):
        del self.labs[course_name]

    def get_section_count(self):
        return len(self.sections)

    def get_section(self, course_name):
        if course_name in self.sections:
            return self.sections[course_name]
        else:
            return None

    def get_lab(self, course_name):
        if course_name in self.labs:
            return self.labs[course_name]
        else:
            return None

    def view_grades(self, username, first_name, last_name):
        display_str = f'\n=========== {first_name.upper()} {last_name.upper()}'\
                  f' GRADES ===========\n'
        for section in self.sections.values():
            display_str += '---------------------------------------------\n'
            display_str += section.course_name + '\n'
            display_str += '---------------------------------------------\n'
            grades = section.get_grades(username)
            if grades:
                grade_str = ', '.join(str(g) for g in grades)
                display_str += f'Grades: {grade_str}\n'
                display_str += f'Average: ' \
                               f'{str(round(sum(grades)/ len(grades)))}\n'
            else:
                display_str += 'No grades recorded for this course\n'
        if not self.sections:
            display_str += 'Student is not currently enrolled in any courses\n'
        display_str += '=============================================\n'
        return display_str

    def view_schedule(self, username, first_name, last_name):
        display_str = f'\n=========== {first_name.upper()} {last_name.upper()}'\
                      f' SCHEDULE ===========\n'
        if self.sections:
            display_str += '---------------------------------------------\n'
            display_str += 'Sections Registered:\n'
            display_str += '---------------------------------------------\n'
            for section in self.sections.values():
                status = section.get_student(username)[1]
                display_str += f'{str(section)} - Registration Status: ' \
                               f'{status}\n'
        if self.labs:
            display_str += '---------------------------------------------\n'
            display_str += 'Labs Registered:\n'
            display_str += '---------------------------------------------\n'
            for lab in self.labs.values():
                status = lab.get_student(username)[1]
                display_str += f'{str(lab)} - Registration Status: {status}\n'
        if not self.sections:
            display_str += 'Student is not currently enrolled in any courses\n'
        display_str += '=============================================\n'
        return display_str


class Instructor(Person):
    """Entity representing an instructor in registration system"""

    def __init__(self, **kwargs):
        super().__init__(kwargs['first_name'], kwargs['last_name'],
                         kwargs['university_id'], kwargs['username'],
                         kwargs['department'])
        self.division = kwargs['division']
        self.is_department_chair = kwargs['is_department_chair']
        self.courses = {}  # key = course_name, value = Course

    def add_course(self, course):
        self.courses[course.name] = course

    def get_course(self, course_name):
        if course_name in self.courses:
            return self.courses[course_name]
        else:
            return None

    def view_courses_teaching(self):
        display_str = f'\n============= {self.first_name.upper()} ' \
                      f'{self.last_name.upper()} COURSES ===============\n'
        display_str += '\n'.join(str(course) for course in
                                self.courses.values())
        display_str += '\n=============================================\n'
        return display_str

    def view_course_students(self, course_name):
        course = self.get_course(course_name)
        if not course:
            return f'Instructor does not teach course: {course_name}'
        else:
            display_str = '\n=================== COURSE ===================\n'
            display_str += course.display_course_students()
            display_str += '\n=============================================\n'
            return display_str
