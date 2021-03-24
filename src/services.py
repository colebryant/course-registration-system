"""
Module: Classes which are "services" that encapsulate domain logic.
Utilizing Strategy pattern for course registration-related functionality.
"""
from abc import ABC, abstractmethod
import db_utils


class RegistrationContext:
    """Context for performing registration actions via a registration strategy
    """

    def __init__(self, student, course, registerable_num, sql_conn,
                 mongo_conn):
        self.student = student
        self.course = course
        self.registerable_num = registerable_num
        self.sql_conn = sql_conn
        self.mongo_conn = mongo_conn
        self.strategy = None

    def set_strategy(self, strategy):
        self.strategy = strategy

    def register(self):
        # Check if course exists
        if not self.course:
            return 'Course not found'
        else:  # Perform remaining logic based on strategy given
            return self.strategy.execute(self.student, self.course,
                                          self.registerable_num,
                                          self.sql_conn, self.mongo_conn)


class IRegistrationStrategy(ABC):
    """Interface for concrete registration strategies"""

    @abstractmethod
    def execute(self, student, course, registerable_num, sql_conn, mongo_conn):
        pass


class SectionRegistration(IRegistrationStrategy):
    """Strategy for student registering in section"""

    def execute(self, student, course, section_number, sql_conn, mongo_conn):
        # Check if student already registered in course section
        if course.find_student_section(student.username):
            return f'Student already registered for section in ' \
                   f'{course.name}'
        # Check if requested section exists
        section = course.get_section(section_number)
        if not section:
            return 'Section not found'
        # Check if section has space remaining
        elif not section.space_remaining:
            return f'Registration denied. Section is full: ' \
                   f'{str(section.max_registration)} ' \
                   f'{str(section.max_registration)} students registered'
        # Check if student is overloading
        elif student.is_fully_registered:
            status = 'Pending'
            section.add_student(student, 'Pending')
            display_str = "Student is overloading on registered " \
                           "classes, and has been added to section as "\
                           "'Pending' before department chair "\
                           "approval."
        # Check if course requires instructor approval
        elif course.approval_required:
            status = 'Tentative'
            section.add_student(student, 'Tentative')
            display_str = f"{course.name} course requires " \
                          f"approval from instructor. Student has " \
                          f"been added to section as 'Tentative' " \
                          f"before instructor approval."
        else:  # No restrictions - student is approved
            status = 'Approved'
            section.add_student(student, 'Approved')
            display_str = f"Student successfully registered for " \
                           f"{course.name} Section " \
                          f"{str(section_number)}"

        # Check if lab required. If so add reminder
        if course.lab_required:
            display_str += '\n**Reminder: Student required to ' \
                           'register for a lab for this course.**'

        # Add section to student's schedule
        student.add_section(section)

        # Add section registration to sql db
        db_utils.db_add_section_reg(status, sql_conn, student.username,
                                    section_number, course.name)
        # Insert log of change in mongo db
        log = f"Student '{student.username}' registered in " \
              f"{course.name} section {str(section.number)} with " \
              f"status '{status}'"
        mongo_conn.insert_log(log)

        return display_str


class LabRegistration(IRegistrationStrategy):
    """Strategy for student registering in lab"""

    def execute(self, student, course, lab_number, sql_conn, mongo_conn):
        # Check if student is already registered in course section
        if not course.find_student_section(student.username):
            return 'Student must first register in a section in ' \
                          f'{course.name} before registering in a lab'
        # Check if student already registered in lab
        if course.find_student_lab(student.username):
            return f'Student already registered for lab in {course.name}. '\
                   f'Please use reschedule lab menu option if you would like '\
                   f'to change into a different lab'
        # Check if requested lab exists
        lab = course.get_lab(lab_number)
        if not lab:
            return 'Lab not found'
        # Check if lab has space remaining
        elif not lab.space_remaining:
            return f'Registration denied. Lab is full: ' \
                   f'{str(lab.max_registration)} / ' \
                   f'{str(lab.max_registration)} students registered',
        # Check if student is overloading
        elif student.is_fully_registered:
            status = 'Pending'
            lab.add_student(student, 'Pending')
            display_str = "Student is overloading on registered classes," \
                           " and has been added to lab as 'Pending' " \
                           "before department chair approval."
        # Check if course requires instructor approval
        elif course.approval_required:
            status = 'Tentative'
            lab.add_student(student, 'Tentative')
            display_str = f"{course.name} course requires approval " \
                           f"from instructor. Student has been added " \
                           f"to lab as 'Tentative' before instructor approval."
        else:  # No restrictions - student is approved
            status = 'Approved'
            lab.add_student(student, 'Approved')
            display_str = f"Student successfully registered for " \
                           f"{course.name} Lab {str(lab_number)}"

        # Add lab to student's schedule
        student.add_lab(lab)

        # Add lab registration to sql db
        db_utils.db_add_lab_reg(status, sql_conn, student.username, lab_number,
                            course.name)

        # Insert log of change in mongo db
        log = f"Student '{student.username}' registered in " \
              f"{course.name} lab {str(lab.number)} with " \
              f"status '{status}'"
        mongo_conn.insert_log(log)

        return display_str


class LabReschedule(IRegistrationStrategy):
    """Strategy for student rescheduling lab"""

    def execute(self, student, course, lab_number, sql_conn, mongo_conn):
        # Check if student is already registered in course section
        if not course.find_student_section(student.username):
            return 'Student must first register in a section in ' \
                          f'{course.name} before registering in a lab'
        # Check if student not already registered in lab
        if not course.find_student_lab(student.username):
            return f'Student is not already registered for lab in ' \
                   f'{course.name}. Please use register in lab menu ' \
                   f'option to register for a lab in this course'
        # Check if requested lab exists
        lab = course.get_lab(lab_number)
        if not lab:
            return 'Lab not found'
        # Check if lab has space remaining
        elif not lab.space_remaining:
            return f'Registration denied. Lab is full: ' \
                   f'{str(lab.max_registration)} / ' \
                   f'{str(lab.max_registration)} students registered',
        # Check if student is overloading
        elif student.is_fully_registered:
            status = 'Pending'
            lab.add_student(student, 'Pending')
            display_str = "Student is overloading on registered classes," \
                           " and has been added to rescheduled lab as " \
                          "'Pending' before department chair approval."
        # Check if course requires instructor approval
        elif course.approval_required:
            status = 'Tentative'
            lab.add_student(student, 'Tentative')
            display_str = f"{course.name} course requires approval " \
                           f"from instructor. Student has been added " \
                           f"to rescheduled lab as 'Tentative' before " \
                          f"instructor approval."
        else:  # No restrictions - student is approved
            status = 'Approved'
            lab.add_student(student, 'Approved')
            display_str = f"Student successfully rescheduled into " \
                           f"{course.name} lab {str(lab_number)}"

        # Add lab to student's schedule
        student.add_lab(lab)

        # Remove old lab registration from sql db
        db_utils.db_delete_lab_reg(sql_conn, course.name, student.username)
        # Add new lab registration to sql db
        db_utils.db_add_lab_reg(status, sql_conn, student.username,
                                lab_number, course.name)

        # Insert log of change in mongo db
        log = f"Student '{student.username}' rescheduled into " \
              f"{course.name} lab {str(lab.number)} with " \
              f"status '{status}'"
        mongo_conn.insert_log(log)

        return display_str


class CourseDropper:
    """Class for student dropping specific course"""

    def __init__(self, student, course_name, sql_conn, mongo_conn):
        self.student = student
        self.course_name = course_name
        self.sql_conn = sql_conn
        self.mongo_conn = mongo_conn

    def drop_course(self):
        schedule = self.student.get_schedule()
        section = schedule.get_section(self.course_name)
        lab = schedule.get_lab(self.course_name)
        # Check if student is registered in course
        if not section and not lab:
            return f'Student is not currently registered in ' \
                   f'{self.course_name}'
        # Check if student registered in section
        if section:
                section.remove_student(self.student.username)
                schedule.remove_section(self.course_name)
        # Check if student registered in lab
        if lab:
            lab.remove_student(self.student.username)
            schedule.remove_lab(self.course_name)

        # Delete course registration from sql db
        db_utils.db_delete_course_reg(self.sql_conn, self.course_name,
                                  self.student.username)

        # Insert log of change in mongo db
        log = f"Student '{self.student.username}' has dropped " \
              f"{self.course_name}"
        self.mongo_conn.insert_log(log)

        return f'Student has successfully dropped {self.course_name}'


class AllCourseDropper:
    """Class for student dropping all courses"""

    def __init__(self, student, sql_conn, mongo_conn):
        self.student = student
        self.sql_conn = sql_conn
        self.mongo_conn = mongo_conn

    def drop_all_courses(self):
        schedule = self.student.get_schedule()
        sections = schedule.sections.values()
        labs = schedule.labs.values()

        # Check that student is registered in a course
        if not sections and not labs:
            return 'Student is not currently registered in any course'
        else:
            for section in sections:
                section.remove_student(self.student.username)
            for lab in labs:
                lab.remove_student(self.student.username)
            schedule.sections = {}
            schedule.labs = {}

            # Delete all student's registrations from sql db
            db_utils.db_delete_all_reg(self.sql_conn, self.student.username)

            # Insert log of change in mongo db
            log = f"Student '{self.student.username}' has dropped all courses"
            self.mongo_conn.insert_log(log)

            return 'Student has successfully dropped all courses from ' \
                   'schedule'


class ApproveDenyRegistration:
    """Class for instructor approving/denying student's registration in a
    course"""

    def __init__(self, instructor, student_username, course_name, is_approved,
                 sql_conn, mongo_conn):
        self.instructor = instructor
        self.student_username = student_username
        self.course_name = course_name
        self.is_approved = is_approved
        self.sql_conn = sql_conn
        self.mongo_conn = mongo_conn

    def approve_deny_reg(self):
        # Check if instructor teaches course
        course = self.instructor.get_course(self.course_name)
        if not course:
            return f'Instructor does not teach {self.course_name}. ' \
                   f'Approve/deny not performed'
        # Check if student is registered in the course
        section = course.find_student_section(self.student_username)
        lab = course.find_student_lab(self.student_username)
        if not section:  # Student is not registered in the course
            return f'Student {self.student_username} not registered in ' \
                   f'{self.course_name}'
        # Get student's current registration status
        student_status = section.get_student(self.student_username)[0]
        #  Only department chair can approve/deny students who are overloading
        if student_status == 'Pending' and not \
                self.instructor.is_department_chair:
            return f"Only department chair can approve / deny 'Pending' " \
                   f"student registrations. No action taken."
        else:  # Otherwise, instructor can approve/deny student
            if self.is_approved:
                section.set_student_status(self.student_username, 'Approved')
                display_str = f"Student '{self.student_username}' is now " \
                              f"approved for {self.course_name} section " \
                              f"{str(section.number)}"
            else:
                section.set_student_status(self.student_username, 'Denied')
                display_str = f"Student '{self.student_username}' has been" \
                               f" denied for {self.course_name} section " \
                               f"{str(section.number)}"

            lab = course.find_student_lab(self.student_username)
            if lab:  # If student registered in lab, approve/deny in lab
                if self.is_approved:
                    lab.set_student_status(self.student_username, 'Approved')
                    display_str += f"\nStudent '{self.student_username}' is " \
                                   f"now approved for {self.course_name} lab "\
                                   f"{str(lab.number)}"
                else:
                    lab.set_student_status(self.student_username, 'Denied')
                    display_str += f"\nStudent '{self.student_username}' has "\
                                   f"been denied for {self.course_name} lab " \
                                   f"{str(lab.number)}"

            # Update status in sql db
            status = 'Approved' if self.is_approved else 'Denied'
            db_utils.db_update_reg_status(status, self.sql_conn,
                                      self.student_username, self.course_name)

            # Insert log of change in mongo db
            log = f"Instructor '{self.instructor.username}' has {status} " \
                  f"student {self.student_username} for {self.course_name}"
            self.mongo_conn.insert_log(log)

            return display_str


class ApprovalRequiredModifier:
    """Class for modifying whether course requires instructor approval"""

    def __init__(self, instructor, course_name, approval_required, sql_conn,
                 mongo_conn):
        self.instructor = instructor
        self.course_name = course_name
        self.approval_required = approval_required
        self.sql_conn = sql_conn
        self.mongo_conn = mongo_conn

    def modify_approval_required(self):
        # Check if instructor teaches course
        course = self.instructor.get_course(self.course_name)
        if not course:
            return f'Instructor does not teach {self.course_name}. Approval ' \
                   f'not modified'
        else:
            course.set_approval_required(self.approval_required)
            if self.approval_required:
                display_str = f'{self.course_name} has been set to instructor'\
                              f' approval required'
            else:
                display_str = f'{self.course_name} has been set to instructor'\
                              f' approval not required'

            # Update approval required in sql db
            app_req = 1 if self.approval_required else 0
            db_utils.db_update_approval_required(self.sql_conn, app_req,
                                             self.course_name)

            # Insert log of change in mongo db
            app_str = "approval required" if self.approval_required else \
                "approval not required"
            log = f"Instructor '{self.instructor.username}' has set " \
                  f"course {self.course_name} to {app_str}"
            self.mongo_conn.insert_log(log)

            return display_str


class Grader:
    """Class for instructor adding a grade to a student's registration in a
    section"""

    def __init__(self, instructor, student_username, course_name, grade,
                 sql_conn, mongo_conn):
        self.instructor = instructor
        self.student_username = student_username
        self.course_name = course_name
        self.grade = grade
        self.sql_conn = sql_conn
        self.mongo_conn = mongo_conn

    def add_grade(self):
        # Check if instructor teaches course
        course = self.instructor.get_course(self.course_name)
        if not course:
            return f'Instructor does not teach {self.course_name}. Grade not '\
                   f'added'
        # Check if student is registered in course
        section = course.find_student_section(self.student_username)
        if not section:
            return f"Student '{self.student_username}' is not registered "\
                   f"in {self.course_name}. Grade not added"
        else:
            section.add_grade(self.student_username, self.grade)
            display_str = f"Grade successfully added to Student " \
                   f"'{self.student_username}' in {self.course_name} section "\
                   f"{str(section.number)}"

            # Add grade to sql db
            db_utils.db_add_grade(self.sql_conn, self.course_name, section.number,
                              self.student_username, self.grade)

            # Insert log of change in mongo db
            log = f"Instructor '{self.instructor.username}' has added " \
                  f"grade: {str(self.grade)} to student " \
                  f"'{self.student_username}' for {self.course_name}"
            self.mongo_conn.insert_log(log)

            return display_str
