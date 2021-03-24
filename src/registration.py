"""
Module: Registration Facade- Access point for client with core system
"""
from people import *
from courses import *
from db_management import *
from services import *


class IRegistrationFacade(ABC):
    """Interface for Registration Facade"""

    # ---------- STUDENT USER FUNCTIONALITY ---------- #

    @abstractmethod
    def view_schedule(self, username) -> str:
        pass

    @abstractmethod
    def view_grades(self, username) -> str:
        pass

    @abstractmethod
    def view_filtered_courses(self, username) -> str:
        pass

    @abstractmethod
    def register_in_section(self, username, course_name, section_number) -> \
            str:
        pass

    @abstractmethod
    def register_in_lab(self, username, course_name, lab_number) -> str:
        pass

    @abstractmethod
    def reschedule_lab(self, username, course_name, lab_number) -> str:
        pass

    @abstractmethod
    def drop_course(self, username, course_name) -> str:
        pass

    @abstractmethod
    def drop_all_courses(self, username) -> str:
        pass

    # -----------INSTRUCTOR USER FUNCTIONALITY ------- #

    @abstractmethod
    def view_courses_teaching(self, username) -> str:
        pass

    @abstractmethod
    def view_course_students(self, username, course_name) -> str:
        pass

    @abstractmethod
    def approve_deny_reg(self, username, student_username, course_name,
                         is_approved) -> str:
        pass

    @abstractmethod
    def modify_approval_required(self, username, course_name, is_required) -> \
            str:
        pass

    @abstractmethod
    def add_grade(self, username, student_username, course_name, grade) -> str:
        pass


class RegistrationFacade(IRegistrationFacade):
    """Facade which provides client access to the registration functionality"""

    def __init__(self, test_mode=False):
        self.student_library = StudentLibrary()  # Singleton - repository of
        # Student objects
        self.instructor_library = InstructorLibrary()  # Singleton -
        # repository of Instructor objects
        self.course_library = CourseLibrary()  # Singleton - repository of
        # Course objects
        self.sql_conn = SQLConnection(test_mode)  # Singleton - SQL connection
        self.mongo_conn = MongoConnection()  # Singleton - MongoDB connection

    def retrieve_data(self):
        """Method which retrieves existing data from SQL database to populate
        the registration system.
        """
        # Open db connection (rather than constantly opening and closing)
        self.sql_conn.open_connection()
        # Get connection to sql database
        sql_conn = self.sql_conn.get_connection()
        # Instantiate SQLRetrieve object for relevant queries passing open sql
        # connection
        sql_retrieve = SQLRetrieve(sql_conn)
        # Populate student_library
        self.student_library.retrieve_data(sql_retrieve)
        # Populate instructor_library
        self.instructor_library.retrieve_data(sql_retrieve)
        # Populate course_library
        self.course_library.retrieve_data(sql_retrieve, self.student_library,
                                          self.instructor_library)
        # Close db connection
        self.sql_conn.close_connection()

    def get_student(self, username):
        return self.student_library.get_student(username)

    def get_instructor(self, username):
        return self.instructor_library.get_instructor(username)

    def get_course(self, course_name):
        return self.course_library.get_course(course_name)

    # ---------- STUDENT USER FUNCTIONALITY ---------- #

    def view_schedule(self, username):
        student = self.get_student(username)
        return student.view_schedule()

    def view_grades(self, username):
        student = self.get_student(username)
        return student.view_grades()

    def view_filtered_courses(self, course_number=None, division=None,
                              instructor_name=None):
        return self.course_library.view_filtered_courses(course_number,
                                                        division,
                                                        instructor_name)

    def register_in_section(self, username, course_name, section_number):
        student = self.get_student(username)
        course = self.get_course(course_name)
        registration_context = RegistrationContext(student, course,
                                                   section_number,
                                                   self.sql_conn,
                                                   self.mongo_conn)
        registration_context.set_strategy(SectionRegistration())
        return registration_context.register()

    def register_in_lab(self, username, course_name, lab_number):
        student = self.get_student(username)
        course = self.get_course(course_name)
        registration_context = RegistrationContext(student, course, lab_number,
                                     self.sql_conn, self.mongo_conn)
        registration_context.set_strategy(LabRegistration())
        return registration_context.register()

    def reschedule_lab(self, username, course_name, lab_number):
        student = self.get_student(username)
        course = self.get_course(course_name)
        registration_context = RegistrationContext(student, course, lab_number,
                                     self.sql_conn, self.mongo_conn)
        registration_context.set_strategy(LabReschedule())
        return registration_context.register()

    def drop_course(self, username, course_name):
        student = self.get_student(username)
        course_dropper = CourseDropper(student, course_name, self.sql_conn,
                                       self.mongo_conn)
        return course_dropper.drop_course()

    def drop_all_courses(self, username):
        student = self.get_student(username)
        all_course_dropper = AllCourseDropper(student, self.sql_conn,
                                              self.mongo_conn)
        return all_course_dropper.drop_all_courses()

    # -----------INSTRUCTOR USER FUNCTIONALITY ------- #

    def view_courses_teaching(self, username):
        instructor = self.get_instructor(username)
        return instructor.view_courses_teaching()

    def view_course_students(self, username, course_name):
        instructor = self.get_instructor(username)
        return instructor.view_course_students(course_name)

    def approve_deny_reg(self, username, student_username, course_name,
                         is_approved):
        instructor = self.get_instructor(username)
        approve_deny_reg = ApproveDenyRegistration(instructor,
                                                   student_username,
                                                   course_name, is_approved,
                                                   self.sql_conn,
                                                   self.mongo_conn)
        return approve_deny_reg.approve_deny_reg()

    def modify_approval_required(self, username, course_name, is_required):
        instructor = self.get_instructor(username)
        app_req_modifier = ApprovalRequiredModifier(instructor, course_name,
                                                    is_required, self.sql_conn,
                                                    self.mongo_conn)
        return app_req_modifier.modify_approval_required()

    def add_grade(self, username, student_username, course_name, grade):
        instructor = self.get_instructor(username)
        grader = Grader(instructor, student_username, course_name, grade,
                        self.sql_conn, self.mongo_conn)
        return grader.add_grade()