"""
Module: Module which includes a set of functions which encapsulate
necessary SQL queries for use in maintaining data permanence. Implemented
as a set of functions since encapsulating in classes is largely unnecessary.
"""
from mysql.connector import Error


def db_add_section_reg(status, sql_conn, student_username, section_number,
                       course_name):
    """Add a student's registration in a section to the SQL db"""
    if not sql_conn.test_mode:
        sql_conn.open_connection()
        try:
            conn = sql_conn.get_connection()
            with conn.cursor() as cursor:
                statement1 = "SELECT ID FROM Student " \
                             f"WHERE UserName = " \
                             f"'{student_username}';"
                cursor.execute(statement1)
                result1 = cursor.fetchone()
                if not result1:
                    return
                student_id = result1[0]
                statement2 = "SELECT s.ID FROM Section s " \
                             "INNER JOIN Course c ON s.CourseID = c.ID " \
                             f"WHERE s.Number = {section_number} " \
                             f"AND c.Name = '{course_name}';"
                cursor.execute(statement2)
                result2 = cursor.fetchone()
                if not result2:
                    return
                section_id = result2[0]
                statement3 = "INSERT INTO SectionStudent " \
                             "(SectionID, StudentID, Status) VALUES " \
                             f"({section_id}, {student_id}, '{status}');"
                cursor.execute(statement3)
                conn.commit()
        except Error as e:
            print(e)
        sql_conn.close_connection()


def db_add_lab_reg(status, sql_conn, student_username, lab_number, course_name):
    """Add a student's registration in a lab to the SQL db"""
    if not sql_conn.test_mode:
        sql_conn.open_connection()
        try:
            conn = sql_conn.get_connection()
            with conn.cursor() as cursor:
                statement1 = "SELECT ID FROM Student " \
                             f"WHERE UserName = '{student_username}';"
                cursor.execute(statement1)
                result1 = cursor.fetchone()
                if not result1:
                    return
                student_id = result1[0]
                statement2 = "SELECT l.ID FROM Lab l " \
                             "INNER JOIN Course c ON l.CourseID = c.ID " \
                             f"WHERE l.Number = {lab_number} " \
                             f"AND c.Name = '{course_name}';"
                cursor.execute(statement2)
                result2 = cursor.fetchone()
                if not result2:
                    return
                lab_id = result2[0]
                statement3 = "INSERT INTO LabStudent " \
                             "(LabID, StudentID, Status) VALUES " \
                             f"({lab_id}, {student_id}, '{status}');"
                cursor.execute(statement3)
                conn.commit()
        except Error as e:
            print(e)
        sql_conn.close_connection()


def db_delete_lab_reg(sql_conn, course_name, student_username):
    """Delete a student's registration in a lab from the SQL db"""
    if not sql_conn.test_mode:
        sql_conn.open_connection()
        conn = sql_conn.get_connection()
        try:
            with conn.cursor() as cursor:
                statement = "DELETE ls FROM LabStudent ls " \
                            "INNER JOIN Student s ON ls.StudentID = s.ID "\
                            "INNER JOIN Lab l ON ls.LabID = " \
                            "l.ID " \
                            "INNER JOIN Course c ON l.CourseID = c.ID " \
                            f"WHERE c.Name = '{course_name}' AND " \
                            f"s.UserName = '{student_username}';"
                cursor.execute(statement)
                conn.commit()
        except Error as e:
            print(e)
        sql_conn.close_connection()


def db_delete_course_reg(sql_conn, course_name, student_username):
    """Delete a student's registration in a course (section and lab)
     from the SQL db"""
    if not sql_conn.test_mode:
        sql_conn.open_connection()
        conn = sql_conn.get_connection()
        try:
            with conn.cursor() as cursor:
                statement1 = "DELETE ss FROM SectionStudent ss " \
                            "INNER JOIN Student s ON ss.StudentID = s.ID "\
                            "INNER JOIN Section sec ON ss.SectionID = " \
                            "sec.ID " \
                            "INNER JOIN Course c ON sec.CourseID = c.ID " \
                            f"WHERE c.Name = '{course_name}' AND " \
                            f"s.UserName = '{student_username}';"
                cursor.execute(statement1)
                statement2 = "DELETE ls FROM LabStudent ls " \
                            "INNER JOIN Student s ON ls.StudentID = s.ID "\
                            "INNER JOIN Lab l ON ls.LabID = " \
                            "l.ID " \
                            "INNER JOIN Course c ON l.CourseID = c.ID " \
                            f"WHERE c.Name = '{course_name}' AND " \
                            f"s.UserName = '{student_username}';"
                cursor.execute(statement2)
                conn.commit()
        except Error as e:
            print(e)
        sql_conn.close_connection()


def db_delete_all_reg(sql_conn, student_username):
    """Delete a student's registration in all courses (sections and labs)
     from the SQL db"""
    if not sql_conn.test_mode:
        sql_conn.open_connection()
        conn = sql_conn.get_connection()
        try:
            with conn.cursor() as cursor:
                statement1 = "DELETE ss FROM SectionStudent ss " \
                            "INNER JOIN Student s ON ss.StudentID = s.ID "\
                            f"WHERE s.UserName = '{student_username}';"
                cursor.execute(statement1)
                statement2 = "DELETE ls FROM LabStudent ls " \
                            "INNER JOIN Student s ON ls.StudentID = s.ID "\
                            f"WHERE s.UserName = '{student_username}';"
                cursor.execute(statement2)
                conn.commit()
        except Error as e:
            print(e)
        sql_conn.close_connection()


def db_update_reg_status(status, sql_conn, student_username,
                         course_name):
    """Update a student's registration status in a course (section and lab)
     in the SQL db"""
    if not sql_conn.test_mode:
        sql_conn.open_connection()
        conn = sql_conn.get_connection()
        try:
            with conn.cursor() as cursor:
                statement1 = "UPDATE SectionStudent ss " \
                             "INNER JOIN Student s ON ss.StudentID = s.ID"\
                             " INNER JOIN Section sec ON ss.SectionID = " \
                             "sec.ID "\
                             "INNER JOIN Course c ON sec.CourseID = c.ID "\
                             f"SET ss.Status = '{status}' " \
                             f"WHERE s.UserName = '{student_username}' " \
                             f"AND c.Name = '{course_name}';"
                cursor.execute(statement1)
                statement2 = "UPDATE LabStudent ls " \
                             "INNER JOIN Student s ON ls.StudentID = s.ID"\
                             " INNER JOIN Lab l ON ls.LabID = l.ID " \
                             "INNER JOIN Course c ON l.CourseID = c.ID "\
                             f"SET ls.Status = '{status}' " \
                             f"WHERE s.UserName = '{student_username}' " \
                             f"AND c.Name = '{course_name}';"
                cursor.execute(statement2)
                conn.commit()
        except Error as e:
            print(e)
        sql_conn.close_connection()


def db_update_approval_required(sql_conn, app_req, course_name):
    """Update a course's approval required state in SQL db"""
    if not sql_conn.test_mode:
        sql_conn.open_connection()
        conn = sql_conn.get_connection()
        try:
            with conn.cursor() as cursor:
                statement = "UPDATE Course " \
                            f"SET ApprovalRequired = {str(app_req)} " \
                            f"WHERE Name = '{course_name}';"
                cursor.execute(statement)
                conn.commit()
        except Error as e:
            print(e)
        sql_conn.close_connection()


def db_add_grade(sql_conn, course_name, section_number, student_username,
                 grade):
    if not sql_conn.test_mode:
        sql_conn.open_connection()
        conn = sql_conn.get_connection()
        try:
            with conn.cursor() as cursor:
                statement1 = "SELECT ID FROM Student " \
                             f"WHERE UserName = '{student_username}';"
                cursor.execute(statement1)
                result1 = cursor.fetchone()
                if not result1:
                    return
                student_id = result1[0]
                statement2 = "SELECT sec.ID FROM Section sec " \
                             "INNER JOIN Course c ON sec.CourseID = c.ID " \
                             f"WHERE sec.Number = {section_number} " \
                             f"AND c.Name = '{course_name}';"
                cursor.execute(statement2)
                result2 = cursor.fetchone()
                if not result2:
                    return
                section_id = result2[0]
                statement3 = "INSERT INTO Grade " \
                             "(SectionID, StudentID, Grade) VALUES " \
                             f"({section_id}, {student_id}, {grade});"
                cursor.execute(statement3)
                conn.commit()
        except Error as e:
            print(e)
        sql_conn.close_connection()