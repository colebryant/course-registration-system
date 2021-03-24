Course Registration System

A mock university course registration system built with a focus on 
object oriented principles and object oriented design patterns.
This project is written in Python, and the required Python packages to be 
installed are ```mysql``` and ```pymongo```.

Design Patterns Used in Project:
- Singleton - Used for database connections as well as repository classes
- Facade - Used for streamlining interaction of client with core system
- Strategy - Used for dynamically switching registration algorithm between
registering in section, registering in lab, or rescheduling lab

Database Setup:

- A MySQL database is utilized for populating system data as well as
maintaining data permanence for the system. To set up, run the included
  SQL scripts (in the sql_scripts directory) in MySQL. The CreateDatabase.sql file
  will create the CourseRegistration database as well as the relevant tables.
  The PopulateTables.sql file will insert pre-existing registration data 
  into the tables. Please note that this system's SQL connection is pointed
  to host: localhost, with username: root and password: parrot123. If 
  necessary, these fields can be changed in the db_management.py file in order
  to successfully connect with the local instance of the MySQL database.
  
- A MongoDB database is utilized for logging changes to data in the
system. The system is connecting to a database called "RegistrationLogging"
  with a single collection called "logging". To create the database,
  run command ```use RegistrationLogging``` followed by command 
  ```db.createCollection("logging")``` in the mongo shell.

Usage Notes:

- Once the databases have been set up, run command ```python client.py``` in the
src directory to start the program. The client is implemented as a simple 
  command line interface. The user begins by entering their username. 
  The user is then  presented with a menu of actions they can take, which
  differs based on whether the user is a student or an instructor. In order
  to perform an action, the user should enter the associated number from the
  menu table. Then the user can follow the prompts to interact with the system.
  
- Student Actions:
  - View Schedule
  - View Grades
  - Search and View Courses
  - Register in Section
  - Register in Lab
  - Reschedule Lab
  - Drop a Course
  - Drop All Courses
  
- Instructor Actions:
  - View Courses Teaching
  - View Students Registered in Course
  - Approve/Deny Student's Registration
  - Modify Course Instructor Approval Required
  - Add Grade to Student

- Existing Courses (currently 1 section and sometimes 1-2 labs per course):
  - Algorithms (Section 1) - Gerry Brady
  - Discrete Mathematics (Section 1) - Gerry Brady
  - Object Oriented Programming (Section 1) - Mark Shacklette
  - Networks (Section 1) - Dave Sahota
    - Has a Lab 1 and Lab 2
  - Financial Accounting (Section 1) - Nikolaev Valeri
  - Perspectives on Computational Analysis (Section 1) - Benjamin Soltoff
    - Has a Lab 1 and Lab 2
  
- Existing Student Usernames and University Enrollment Status:
  - cbryant - Full-Time
  - jmoran - Full-Time
  - brhodes - Full-Time
  - mcabrera - Full-Time
  - natkins - Part-Time
  - dwhitley - Part-Time
  - kkane - Part-Time
  - ssoto - Full-Time
  - kmacleod - Full-Time
  - awhite - Full-Time
  - mbaxter - Part-Time
  - agates - Part-Time
  - cbates - Full-Time
  - wwilson - Full-Time
  - jarcher - Part-Time
  - dnixon - Part-Time
  - mfritz - Part-Time
  
- Existing Instructor Usernames and Department Chair Status:
  - gbrady - Department Chair
  - mshacklette - Department Chair
  - dsahota - Not Department Chair
  - nvaleri - Not Department Chair
  - bsoltoff - Department Chair

Recommended usernames for use in testing (varied data already exists):

- Login with username 'cbryant' for student user functionality
- Login with username 'gbrady' for instructor user functionality

