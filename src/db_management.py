"""
Module: Classes associated with database management context
"""
from mysql.connector import connect, Error
from pymongo import MongoClient
from datetime import datetime


class SQLConnection:
    """SQL database connection object. Implemented as Singleton"""
    __instance__ = None

    def __init__(self, test_mode):
        if SQLConnection.__instance__ is None:
            self._host = 'localhost'
            self._username = 'root'
            self._password = 'parrot123'
            self._database = 'CourseRegistration'
            self.test_mode = test_mode
            self._conn = None
            SQLConnection.__instance__ = self
        else:
            raise Exception('Cannot create another SQLConnection class')

    def open_connection(self):
        try:
            conn = connect(
                host=self._host,
                user=self._username,
                password=self._password,
                database=self._database
            )
            self._conn = conn

        except Error as e:
            print(e)
            self._conn = None

    def get_connection(self):
        return self._conn

    def close_connection(self):
        self._conn.close()


class MongoConnection:
    """MongoDB database connection object. Implemented as Singleton"""
    __instance__ = None

    def __init__(self):
        if MongoConnection.__instance__ is None:
            self._client = MongoClient()
            self._db = self._client.RegistrationLogging
            MongoConnection.__instance__ = self
        else:
            raise Exception('Cannot create another MongoConnection class')

    def insert_log(self, log):
        log_dict = {
            'time': datetime.now(),
            'log': log
        }
        logging = self._db.logging
        logging.insert_one(log_dict)


class SQLRetrieve:
    """Class which encapsulates queries to retrieve system data from SQL
    database. Takes in opened sql connection so that multiple selects can be
    performed without continually opening and closing database connection."""

    def __init__(self, conn):
        self._conn = conn

    def get_students(self):
        try:
            student_list = []
            with self._conn.cursor() as cursor:
                statement = "SELECT * FROM Student;"
                cursor.execute(statement)
                result = cursor.fetchall()
                for row in result:
                    student_list.append({
                        'university_id': int(row[1]),
                        'username': row[2],
                        'first_name': row[3],
                        'last_name': row[4],
                        'major': row[5],
                        'program': row[6],
                        'department': row[7],
                        'is_full_time': True if int(row[8]) == 1 else False
                    })
            return student_list
        except Error as e:
            print(e)

    def get_instructors(self):
        try:
            instructor_list = []
            with self._conn.cursor() as cursor:
                statement = "SELECT * FROM Instructor;"
                cursor.execute(statement)
                result = cursor.fetchall()
                for row in result:
                    instructor_list.append({
                        'university_id': int(row[1]),
                        'username': row[2],
                        'first_name': row[3],
                        'last_name': row[4],
                        'division': row[5],
                        'department': row[6],
                        'is_department_chair': True if int(row[7]) == 1 else
                        False
                    })
            return instructor_list
        except Error as e:
            print(e)

    def get_courses(self):
        try:
            course_list = []
            with self._conn.cursor() as cursor:
                statement = "SELECT i.FirstName, i.LastName, i.UserName, c.* "\
                        "FROM COURSE c INNER JOIN Instructor i ON " \
                            "c.InstructorID = i.ID;"
                cursor.execute(statement)
                result = cursor.fetchall()
                for row in result:
                    course_list.append({
                        'instructor_name': row[0] + ' ' + row[1],
                        'instructor_username': row[2],
                        'number': int(row[5]),
                        'name': row[6],
                        'division': row[7],
                        'department': row[8],
                        'program': row[9],
                        'lab_required': True if int(row[10]) == 1 else False,
                        'approval_required': True if int(row[11]) == 1 else
                        False
                    })
            return course_list
        except Error as e:
            print(e)

    def get_sections(self):
        try:
            section_list = []
            with self._conn.cursor() as cursor:
                statement = "SELECT c.name, s.* FROM Section s " \
                            "INNER JOIN Course c ON s.CourseID = c.ID;"
                cursor.execute(statement)
                result = cursor.fetchall()
                for row in result:
                    section_list.append({
                        'course_name': row[0],
                        'section_number': int(row[3]),
                        'max_registration': int(row[4]),
                        'time': row[5],
                        'day': row[6]
                    })
            return section_list
        except Error as e:
            print(e)

    def get_labs(self):
        try:
            lab_list = []
            with self._conn.cursor() as cursor:
                statement = "SELECT c.name, l.* FROM Lab l " \
                            "INNER JOIN Course c ON l.CourseID = c.ID;"
                cursor.execute(statement)
                result = cursor.fetchall()
                for row in result:
                    lab_list.append({
                        'course_name': row[0],
                        'lab_number': int(row[3]),
                        'max_registration': int(row[4]),
                        'time': row[5],
                        'day': row[6]
                    })
            return lab_list
        except Error as e:
            print(e)

    def get_section_students(self, course_name, section_number):
        try:
            section_students = []
            with self._conn.cursor() as cursor:
                statement = "SELECT s.UserName, ss.Status FROM " \
                            "SectionStudent ss " \
                            "INNER JOIN Section sec ON ss.SectionID = sec.ID "\
                            "INNER JOIN Course c ON sec.CourseID = c.ID " \
                            "INNER JOIN Student s ON ss.StudentID = s.ID " \
                            f"WHERE sec.Number = {str(section_number)} AND " \
                            f"c.Name = '{course_name}';"
                cursor.execute(statement)
                result = cursor.fetchall()
                for row in result:
                    section_students.append({
                        'student_username': row[0],
                        'status': row[1],
                    })
            return section_students
        except Error as e:
            print(e)

    def get_lab_students(self, course_name, lab_number):
        try:
            lab_students = []
            with self._conn.cursor() as cursor:
                statement = "SELECT s.UserName, ls.Status FROM " \
                            "LabStudent ls " \
                            "INNER JOIN Lab l ON ls.LabID = l.ID "\
                            "INNER JOIN Course c ON l.CourseID = c.ID " \
                            "INNER JOIN Student s ON ls.StudentID = s.ID " \
                            f"WHERE l.Number = {str(lab_number)} AND " \
                            f"c.Name = '{course_name}';"
                cursor.execute(statement)
                result = cursor.fetchall()
                for row in result:
                    lab_students.append({
                        'student_username': row[0],
                        'status': row[1],
                    })
            return lab_students
        except Error as e:
            print(e)

    def get_section_grades(self, course_name, section_number):
        try:
            section_grades = []
            with self._conn.cursor() as cursor:
                statement = "SELECT g.Grade, s.UserName FROM Grade g " \
                            "INNER JOIN Student s ON g.StudentID = s.ID " \
                            "INNER JOIN Section sec ON g.SectionID = sec.ID " \
                            "INNER JOIN Course c ON sec.CourseID = c.ID " \
                            f"WHERE sec.Number = {str(section_number)} AND " \
                            f"c.Name = '{course_name}';"
                cursor.execute(statement)
                result = cursor.fetchall()
                for row in result:
                    section_grades.append({
                        'grade': row[0],
                        'student_username': row[1]
                    })
            return section_grades
        except Error as e:
            print(e)





