"""
Module: Entities relating to Course Management Bounded Context
"""
from abc import ABC


class CourseLibrary:
    """Repository for courses. Implemented as singleton"""
    __instance__ = None

    def __init__(self):
        if CourseLibrary.__instance__ is None:
            self.courses = {}  # dict of Courses: key = course_name, value =
            # Course
        else:
            raise Exception('Cannot create another CourseLibrary class')

    def retrieve_data(self, sql_retrieve, student_lib, instructor_lib):
        # Populate courses
        course_list = sql_retrieve.get_courses()
        for c in course_list:
            current_course = self.add_course(**c)
            # Add course to relevant instructor
            course_instructor = instructor_lib.get_instructor\
                (c['instructor_username'])
            course_instructor.add_course(current_course)

        # Populate sections
        section_list = sql_retrieve.get_sections()
        for s in section_list:
            # Add section to course_library
            current_section = self.add_section(**s)
            # Add section to students' schedules and students to section roster
            section_students = sql_retrieve.get_section_students(
                s['course_name'], s['section_number'])
            if section_students:
                for st in section_students:
                    current_student = student_lib.get_student(st['student_username'])
                    current_student.add_section(current_section)
                    current_section.add_student(current_student, st['status'])
            # Add section grades to section's gradebook
            section_grades = sql_retrieve.get_section_grades(
                s['course_name'], s['section_number'])
            if section_grades:
                for g in section_grades:
                    current_section.add_grade(g['student_username'],
                                              g['grade'])

        # Populate labs
        lab_list = sql_retrieve.get_labs()
        for l in lab_list:
            # Add lab to course_library
            current_lab = self.add_lab(**l)
            # Add lab to students' schedules and students to lab roster
            lab_students = sql_retrieve.get_lab_students(
                l['course_name'], l['lab_number'])
            if lab_students:
                for st in lab_students:
                    current_student = student_lib.get_student\
                        (st['student_username'])
                    current_student.add_lab(current_lab)
                    current_lab.add_student(current_student, st['status'])

    def add_course(self, **kwargs):
        new_course = Course(**kwargs)
        self.courses[kwargs['name']] = new_course
        return new_course

    def add_section(self, **kwargs):
        return self.courses[kwargs['course_name']].add_section(**kwargs)

    def add_lab(self, **kwargs):
        return self.courses[kwargs['course_name']].add_lab(**kwargs)

    def get_course(self, course_name):
        if course_name in self.courses:
            return self.courses[course_name]
        else:
            return None

    def view_filtered_courses(self, course_number, division, instructor_name):
        # Optionally filter by course number, division, and instructor name
        course_list = list(filter(lambda x:
            (x.number == int(course_number) if course_number else True) and
            (x.division == division if division else True) and
            (x.instructor_name == instructor_name if instructor_name else True)
            , self.courses.values()))

        if not course_list:
            return 'No courses found matching criteria'

        display_str = '\n=============== SEARCH RESULTS ==============\n'
        for course in course_list:
            display_str += '\n=================== COURSE ==================\n'
            display_str += course.display_course_detail()
            display_str += '=============================================\n'

        return display_str


class Course:
    """Entity representing course which is composed of sections and labs"""

    def __init__(self, **kwargs):
        self.number = kwargs['number']
        self.name = kwargs['name']
        self.department = kwargs['department']
        self.division = kwargs['division']
        self.program = kwargs['program']
        self.lab_required = kwargs['lab_required']
        self.instructor_name = kwargs['instructor_name']
        self.approval_required = kwargs['approval_required']
        self.sections = {}  # dict of sections: key = section_number, value =
        # Section
        self.labs = {}  # dict of labs: key = lab_number, value =
        # Lab

    def add_section(self, **kwargs):
        new_section = Section(kwargs['section_number'], self.name, self.number,
                              self.program, self.instructor_name,
                              kwargs['max_registration'], kwargs['time'],
                              kwargs['day'])
        self.sections[kwargs['section_number']] = new_section
        return new_section

    def add_lab(self, **kwargs):
        new_lab = Lab(kwargs['lab_number'], self.name, self.number,
                              self.program, self.instructor_name,
                              kwargs['max_registration'], kwargs['time'],
                              kwargs['day'])
        self.labs[kwargs['lab_number']] = new_lab
        return new_lab

    def get_section(self, section_number):
        if section_number in self.sections:
            return self.sections[section_number]
        else:
            return None

    def get_lab(self, lab_number):
        if lab_number in self.labs:
            return self.labs[lab_number]
        else:
            return None

    def set_approval_required(self, is_required):
        self.approval_required = is_required

    def find_student_section(self, username):
        student_section = None
        for section in self.sections.values():
            if section.is_student_in_registerable(username):
                student_section = section
                break
        return student_section

    def find_student_lab(self, username):
        student_lab = None
        for lab in self.labs.values():
            if lab.is_student_in_registerable(username):
                student_lab = lab
                break
        return student_lab

    def display_course_students(self):
        students = set()
        for section in self.sections.values():
            for student in section.get_all_students():
                students.add(student)
        if self.labs:
            for lab in self.labs.values():
                for student in lab.get_all_students():
                    students.add(student)

        display_str = str(self)
        display_str += '\n---------------------------------------------'
        display_str += '\nStudents Registered:\n'
        display_str += '---------------------------------------------\n'
        display_str += '\n'.join(f'{str(student[0])}, Status: {student[1]}'
                                 for student in students)
        return display_str

    def display_course_detail(self):
        display_str = str(self)
        display_str += '\n---------------------------------------------'
        display_str += '\nSections:\n'
        display_str += '---------------------------------------------\n'
        display_str += '\n'.join(str(section) for section in
                                self.sections.values())
        display_str += '\n'
        if self.labs:
            display_str += '---------------------------------------------\n'
            display_str += 'Labs:\n'
            display_str += '---------------------------------------------\n'
            display_str += '\n'.join(str(lab) for lab in
                                                   self.labs.values()) + '\n'
        return display_str

    def __str__(self):  # Course: MPCS 55001: Algorithms - Gerry Brady,
        # Instructor Approval Required
        display_str = f'{self.program} {str(self.number)}: {self.name} - '\
               f'{self.instructor_name}'
        if self.approval_required:
            display_str += ', Instructor Approval Required'
        return display_str


class Registerable(ABC):
    """Abstract Base Class for 'registerable' entities (Section & Lab)"""

    def __init__(self, number, course_name, course_number, course_program,
                 course_instructor, max_registration, time, day):
        self.number = number
        self.course_name = course_name
        self.course_number = course_number
        self.course_program = course_program
        self.course_instructor = course_instructor
        self.registered_students = {}  # key: username, value: (Student,
        # status of registration)
        self.max_registration = max_registration
        self.time = time
        self.day = day

    @property
    def space_remaining(self):
        total_registered = len(self.registered_students)
        if total_registered < self.max_registration:
            return True
        else:
            return False

    def add_student(self, student, status):
        self.registered_students[student.username] = (student, status)

    def remove_student(self, username):
        del self.registered_students[username]

    def set_student_status(self, username, status):
        self.registered_students[username] = \
            (self.registered_students[username][0], status)

    def get_student(self, username):
        return self.registered_students[username]

    def get_all_students(self):
        return list(self.registered_students.values())

    def is_student_in_registerable(self, username):
        return username in self.registered_students


class Section(Registerable):
    """Entity representing a section of a course"""

    def __init__(self, number, course_name, course_number, course_program,
                 course_instructor, max_registration, time, day):
        super().__init__(number, course_name, course_number, course_program,
                 course_instructor, max_registration, time, day)
        self.grade_book = GradeBook()

    def add_grade(self, username, grade):
        self.grade_book.add_grade(username, grade)

    def get_grades(self, username):
        return self.grade_book.get_grades(username)

    def __str__(self):  # Section: MPCS 55001-1: Algorithms, Gerry Brady,
        # Tuesday 2:30PM, Enrollment: 5/10
        return f'{self.course_program} {str(self.course_number)}-'\
               f'{str(self.number)}: {self.course_name} - ' \
               f'{self.course_instructor}, {self.day} {self.time}, ' \
               f'Enrollment: {str(len(self.registered_students))}/' \
               f'{str(self.max_registration)}'


class GradeBook:
    """Entity representing grade book for section"""

    def __init__(self):
        self.grades = {}  # key = username, value = list of grades

    def add_grade(self, username, grade):
        if username in self.grades:
            self.grades[username].append(grade)
        else:
            self.grades[username] = [grade]

    def get_grades(self, username):
        if username in self.grades:
            return self.grades[username]
        else:
            return None


class Lab(Registerable):
    """Entity which represents a lab"""

    def __init__(self, number, course_name, course_number, course_program,
                 course_instructor, max_registration, time, day):
        super().__init__(number, course_name, course_number, course_program,
                 course_instructor, max_registration, time, day)

    def __str__(self):  #Lab: MPCS 55001-Lab1: Algorithms, Gerry Brady,
        # Monday 4:30PM, Enrollment: 0/10
        return f'{self.course_program} {str(self.course_number)}-Lab' \
               f'{str(self.number)}: {self.course_name} - ' \
               f'{self.course_instructor}, {self.day} {self.time}, ' \
               f'Enrollment: {str(len(self.registered_students))}/' \
               f'{str(self.max_registration)}'





