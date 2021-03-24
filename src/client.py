"""
Module: Command line client interface for interacting with registration system.
Performs some input validation and prints relevant information.
Interaction with core system is performed via the Registration Facade.
"""
from registration import RegistrationFacade

reg = RegistrationFacade()
reg.retrieve_data()
print('=============================================')
print('Welcome to the Course Registration System!')
print('=============================================')

while True:
    username = input("[Enter 'E' to exit] Please enter your username: ")
    if username == 'E':
        break
    elif reg.get_student(username):
        is_student = True
        valid_username = True
    elif reg.get_instructor(username):
        is_student = False
        valid_username = True
    else:
        valid_username = False
        print('Invalid username. Please try again')

    if valid_username:
        if is_student:
            while True:
                student_menu = '============================================='\
                               '\n'\
                               'Student Menu\n' \
                               '---------------------------------------------'\
                               '\n'\
                               '(1) - View Schedule\n' \
                               '(2) - View Grades\n' \
                               '(3) - Search and View Courses\n' \
                               '(4) - Register in Section\n' \
                               '(5) - Register in Lab\n' \
                               '(6) - Reschedule Lab\n' \
                               '(7) - Drop a Course\n' \
                               '(8) - Drop All Courses\n' \
                               '============================================='
                print(student_menu)
                answer = input("[Enter 'L' to logout] Press any key to "
                               "continue: ")
                if answer == 'L':
                    break
                while True:
                    while True:
                        menu_choice = input("[Enter 'M' to see menu again] "
                                            "Please enter number for desired "
                                            "menu action: ")
                        if menu_choice == 'M':
                            break
                        valid_choices = [1, 2, 3, 4, 5, 6, 7, 8]
                        if not menu_choice.isnumeric() or int(menu_choice) not\
                                in valid_choices:
                            print('Please enter a number between 1 and 8')
                        else:
                            break
                    if menu_choice == 'M':
                        break
                    menu_choice = int(menu_choice)
                    if menu_choice == 1:
                        print(reg.view_schedule(username))
                    elif menu_choice == 2:
                        print(reg.view_grades(username))
                    elif menu_choice == 3:
                        print('To Search Course Library:')
                        while True:
                            course_number = input('Enter course number, or '
                                                  'press enter to leave filter '
                                                  'blank: ')
                            if not course_number or course_number.isnumeric():
                                break
                            else:
                                print('If filtering by course number, please '
                                      'enter a valid integer')
                        division = input('Enter division, or press enter to '
                                         'leave filter blank: ')
                        instructor_name = input('Enter instructor full name, '
                                                'or press enter to leave '
                                                'filter blank: ')
                        print(reg.view_filtered_courses(course_number,
                                                        division,
                                                        instructor_name))
                    elif menu_choice == 4:
                        print('To Register in Section:')
                        course_name = input('Enter course name: ')
                        while True:
                            section_number = input('Enter section number: ')
                            if not section_number.isnumeric():
                                print('Please enter a valid integer for '
                                      'section number')
                            else:
                                break
                        print(reg.register_in_section(username, course_name,
                                                      int(section_number)))
                    elif menu_choice == 5:
                        print('To Register in Lab:')
                        course_name = input('Enter course name: ')
                        while True:
                            lab_number = input('Enter lab number: ')
                            if not lab_number.isnumeric():
                                print('Please enter a valid integer for lab '
                                      'number')
                            else:
                                break
                        print(reg.register_in_lab(username, course_name,
                                                  int(lab_number)))
                    elif menu_choice == 6:
                        print('To Reschedule Lab:')
                        course_name = input('Enter course name: ')
                        while True:
                            lab_number = input('Enter number of lab you '
                                                   'would like to switch to: ')
                            if not lab_number.isnumeric():
                                print('Please enter a valid integer for '
                                      'lab number')
                            else:
                                break
                        print(reg.reschedule_lab(username, course_name,
                                                 int(lab_number)))
                    elif menu_choice == 7:
                        print('To Drop Course:')
                        course_name = input('Enter course name: ')
                        print(reg.drop_course(username, course_name))
                    elif menu_choice == 8:
                        while True:
                            answer = input("Are you sure you want to drop all "
                                           "courses? Y/N: ")
                            valid_choices = ['Y', 'N']
                            if answer not in valid_choices:
                                print('Please respond with Y or N')
                            else:
                                break
                        if answer == 'Y':
                            print(reg.drop_all_courses(username))

        else:
            while True:
                instr_menu = '=============================================\n'\
                               'Instructor Menu\n' \
                             '---------------------------------------------' \
                             '\n' \
                             '(1) - View Courses Teaching\n' \
                               '(2) - View Students Registered in Course\n' \
                               "(3) - Approve/Deny Student's Registration\n" \
                               '(4) - Modify Course Instructor Approval ' \
                             'Required\n' \
                               '(5) - Add Grade to Student\n' \
                               '============================================='
                print(instr_menu)
                answer = input("[Enter 'L' to logout] Press any key to "
                               "continue: ")
                if answer == 'L':
                    break
                while True:
                    while True:
                        menu_choice = input("[Enter 'M' to see menu again] "
                                            "Please enter number for desired "
                                            "menu action: ")
                        if menu_choice == 'M':
                            break
                        valid_choices = [1, 2, 3, 4, 5]
                        if not menu_choice.isnumeric() or int(menu_choice) not\
                                in valid_choices:
                            print('Please enter a number between 1 and 5')
                        else:
                            break
                    if menu_choice == 'M':
                        break
                    menu_choice = int(menu_choice)
                    if menu_choice == 1:
                        print(reg.view_courses_teaching(username))
                    elif menu_choice == 2:
                        course_name = input('Enter course name: ')
                        print(reg.view_course_students(username, course_name))
                    elif menu_choice == 3:
                        print("To Approve/Deny a Student's Registration:")
                        course_name = input('Enter course name: ')
                        student_username = input('Enter the username of the '
                                                 'student: ')
                        while True:
                            answer = input("Enter 'A' to approve student or "
                                           "'D' to deny student: ")
                            valid_choices = ['A', 'D']
                            if answer not in valid_choices:
                                print("Please enter a valid letter")
                            else:
                                break
                        is_approved = True if answer == 'A' else False
                        print(reg.approve_deny_reg(username, student_username,
                                                   course_name, is_approved))
                    elif menu_choice == 4:
                        print("To Modify Whether Course Requires Instructor "
                              "Approval:")
                        course_name = input('Enter course name: ')
                        while True:
                            answer = input("Enter 'Y' to require approval or "
                                           "'N' to not require approval: ")
                            valid_choices = ['Y', 'N']
                            if answer not in valid_choices:
                                print("Please enter a valid letter")
                            else:
                                break
                        approval_required = True if answer == 'Y' else False
                        print(reg.modify_approval_required(username,
                                                           course_name,
                                                           approval_required))
                    elif menu_choice == 5:
                        print("To Add Grade to Student in Course:")
                        course_name = input('Enter course name: ')
                        student_username = input('Enter the username of the '
                                                 'student: ')
                        while True:
                            answer = input("Enter a grade (0 - 100): ")
                            valid_choices = [i for i in range(101)]

                            if not answer.isnumeric() or int(answer) not in \
                                    valid_choices:
                                print("Please enter a numeric grade between"
                                      " 0 and 100")
                            else:
                                break
                        grade = int(answer)
                        print(reg.add_grade(username, student_username,
                                            course_name, grade))
