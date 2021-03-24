-- Script for populating existing tables with data. Must be run after creating
-- database and tables.

/*
DELETE FROM SectionStudent;
DELETE FROM LabStudent;
DELETE FROM Grade;
DELETE FROM Section;
DELETE FROM Lab;
DELETE FROM Course;
DELETE FROM Instructor;
DELETE FROM Student;
*/

-- Populate Student Table
INSERT INTO Student (UniversityID, UserName, FirstName, LastName, Major, Program, Department, IsFullTime)
VALUES (47993572, 'cbryant', 'Cole', 'Bryant', 'Computer Science', 'MPCS', 'Computer Science', 1),
(83279016, 'jmoran', 'Jeff', 'Moran', 'Computer Science', 'MPCS', 'Computer Science', 1),
(84258006, 'brhodes', 'Brandi', 'Rhodes', 'Computer Science', 'MPCS', 'Computer Science', 1),
(71452986, 'mcabrera', 'Melinda', 'Cabrera', 'Computer Science', 'MPCS', 'Computer Science', 1),
(94490916, 'natkins', 'Nyle', 'Atkins', 'Computer Science', 'MPCS', 'Computer Science', 0),
(68095629, 'dwhitley', 'Dennis', 'Whitley', 'Computer Science', 'MPCS', 'Computer Science', 0),
(47005398, 'kkane', 'Kathryn', 'Kane', 'Computer Science', 'MPCS', 'Computer Science', 0),
(20740108, 'ssoto', 'Saul', 'Soto', 'Computational Social Science', 'MACSS', 'Social Sciences', 1),
(42684346, 'kmacleod', 'Kamile', 'Macleod', 'Computational Social Science', 'MACSS', 'Social Sciences', 1),
(51201411, 'awhite', 'Annalise', 'White', 'Computational Social Science', 'MACSS', 'Social Sciences', 1),
(27954021, 'mbaxter', 'Mysha', 'Baxter', 'Computational Social Science', 'MACSS', 'Social Sciences', 0),
(66165874, 'agates', 'Ariah', 'Gates', 'Computational Social Science', 'MACSS', 'Social Sciences', 0),
(56967312, 'cbates', 'Cally', 'Bates', 'Business', 'Booth', 'Business', 1),
(76338942, 'wwilson', 'William', 'Wilson', 'Business', 'Booth', 'Business', 1),
(20792781, 'jarcher', 'Jarred', 'Archer', 'Business', 'Booth', 'Business', 0),
(44947079, 'dnixon', 'Debbie', 'Nixon', 'Business', 'Booth', 'Business', 0),
(62357057, 'mfritz', 'Mikhail', 'Fritz', 'Business', 'Booth', 'Business', 0);

-- Populate Instructor Table
INSERT INTO Instructor (UniversityID, UserName, FirstName, LastName, Division, Department, IsDepartmentChair)
VALUES (70398398, 'gbrady', 'Gerry', 'Brady', 'Physical Sciences', 'Computer Science', 1),
(34572183, 'mshacklette', 'Mark', 'Shacklette', 'Physical Sciences', 'Computer Science', 1),
(92101807, 'dsahota', 'Dave', 'Sahota', 'Physical Sciences', 'Computer Science', 0),
(34572183, 'nvaleri', 'Nikolaev', 'Valeri', 'Booth', 'Business', 0),
(19907807, 'bsoltoff', 'Benjamin', 'Soltoff', 'Social Sciences', 'Social Sciences', 1);

-- Populate Course Table
INSERT INTO Course(InstructorID, Number, Name, Division, Department, Program, LabRequired, ApprovalRequired)
VALUES (1, 55001, 'Algorithms', 'Physical Sciences', 'Computer Science', 'MPCS', 0, 1),
(1, 50103, 'Discrete Mathematics', 'Physical Sciences', 'Computer Science', 'MPCS', 0, 0),
(2, 51410, 'Object Oriented Programming', 'Physical Sciences', 'Computer Science', 'MPCS', 0, 0),
(3, 54001, 'Networks', 'Physical Sciences', 'Computer Science', 'MPCS', 1, 0),
(4, 30000, 'Financial Accounting', 'Booth', 'Business', 'Booth', 0, 0),
(5, 30000, 'Perspectives on Computational Analysis', 'Social Sciences', 'Computer Science', 'MACSS', 1, 1);

-- Populate Section Table
INSERT INTO Section(CourseID, Number, MaxRegistration, Time, Day)
VALUES (1, 1, 10, '2:30PM', 'Tuesday'),
(2, 1, 10, '5:30PM', 'Wednesday'),
(3, 1, 10, '5:30PM', 'Monday'),
(4, 1, 10, '5:30PM', 'Thursday'),
(5, 1, 10, '2:00PM', 'Thursday'),
(6, 1, 10, '2:30PM', 'Friday');

-- Populate Lab Table
INSERT INTO Lab(CourseID, Number, MaxRegistration, Time, Day)
VALUES (4, 1, 10, '7:00PM', 'Thursday'),
(4, 2, 10, '8:30AM', 'Friday'),
(6, 1, 10, '4:30PM', 'Friday'),
(6, 2, 10, '10:30AM', 'Saturday');

-- Populate SectionStudent Table
INSERT INTO SectionStudent(SectionID, StudentID, Status)
VALUES (1, 1, 'Approved'),
(1, 2, 'Approved'),
(1, 3, 'Tentative'),
(1, 4, 'Approved'),
(1, 5, 'Tentative'),
(1, 6, 'Approved'),
(1, 7, 'Approved'),
(2, 1, 'Approved'),
(2, 2, 'Approved'),
(2, 3, 'Approved'),
(2, 4, 'Approved'),
(2, 5, 'Approved'),
(2, 6, 'Approved'),
(2, 7, 'Approved'),
(2, 8, 'Approved'),
(2, 9, 'Approved'),
(2, 10, 'Approved'),
(3, 11, 'Approved'),
(3, 12, 'Approved'),
(4, 1, 'Approved'),
(4, 2, 'Approved'),
(5, 11, 'Approved'),
(5, 12, 'Approved'),
(6, 3, 'Tentative'),
(6, 4, 'Tentative');

-- Populate LabStudent Table
INSERT INTO LabStudent(LabID, StudentID, Status)
VALUES (1, 1, 'Approved'),
(1, 2, 'Approved'),
(2, 3, 'Tentative'),
(2, 4, 'Tentative');

-- Populate Grade Table
INSERT INTO Grade(SectionID, StudentID, Grade)
VALUES (1, 1, 95),
(1, 1, 85),
(1, 2, 95),
(1, 2, 85),
(1, 3, 95),
(1, 3, 85),
(1, 4, 95),
(1, 4, 85),
(1, 5, 95),
(1, 5, 85),
(1, 6, 95),
(1, 6, 85),
(1, 7, 95),
(1, 7, 85),
(2, 1, 95),
(2, 1, 85),
(2, 2, 95),
(2, 2, 85),
(2, 3, 95),
(2, 3, 85),
(2, 4, 95),
(2, 4, 85),
(2, 5, 95),
(2, 5, 85),
(2, 6, 95),
(2, 6, 85),
(2, 7, 95),
(2, 7, 85),
(2, 8, 95),
(2, 8, 85),
(2, 9, 95),
(2, 9, 85),
(2, 10, 95),
(2, 10, 85);