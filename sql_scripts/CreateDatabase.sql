-- Script for creating tables in CourseRegistration database. Must be run prior to table inserts.

-- Create and Switch to CourseRegistration Database
CREATE DATABASE IF NOT EXISTS CourseRegistration;
USE CourseRegistration;

/*
DROP TABLE IF EXISTS SectionStudent;
DROP TABLE IF EXISTS LabStudent;
DROP TABLE IF EXISTS Grade;
DROP TABLE IF EXISTS Section;
DROP TABLE IF EXISTS Lab;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Instructor;
DROP TABLE IF EXISTS Student;
*/

-- Create Instructor Table
CREATE TABLE Instructor(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
	,UniversityID INT NOT NULL
	,UserName VARCHAR(30) NOT NULL
	,FirstName VARCHAR(30)
	,LastName VARCHAR(30)
	,Division VARCHAR(30)
	,Department VARCHAR(30)
	,IsDepartmentChair BOOLEAN NOT NULL DEFAULT 0
);

-- Create Student Table
CREATE TABLE Student(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
	,UniversityID INT NOT NULL
	,UserName VARCHAR(30) NOT NULL
	,FirstName VARCHAR(30)
	,LastName VARCHAR(30)
	,Major VARCHAR(30)
	,Program VARCHAR(30)
	,Department VARCHAR(30)
	,IsFullTime BOOLEAN NOT NULL DEFAULT 1
);

-- Create Course Table
CREATE TABLE Course(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
	,InstructorID INT
	,Number INT NOT NULL
	,Name VARCHAR(50) NOT NULL
	,Division VARCHAR(30)
	,Department VARCHAR(30)
	,Program VARCHAR(30)
	,LabRequired BOOLEAN NOT NULL DEFAULT 0
	,ApprovalRequired BOOLEAN NOT NULL DEFAULT 0
	,FOREIGN KEY (InstructorID) REFERENCES Instructor(ID)
);

-- Create Section Table
CREATE TABLE Section(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
	,CourseID INT
	,Number INT NOT NULL
	,MaxRegistration INT
	,Time VARCHAR(30)
	,Day VARCHAR(30)
	,FOREIGN KEY (CourseID) REFERENCES Course(ID)
);

-- Create Lab Table
CREATE TABLE Lab(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
	,CourseID INT
	,Number INT NOT NULL
	,MaxRegistration INT
	,Time VARCHAR(30)
	,Day VARCHAR(30)
	,FOREIGN KEY (CourseID) REFERENCES Course(ID)
);

-- Create SectionStudent Table
CREATE TABLE SectionStudent(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
	,SectionID INT NOT NULL
	,StudentID INT NOT NULL
	,Status VARCHAR(30)
	,FOREIGN KEY (SectionID) REFERENCES Section(ID)
	,FOREIGN KEY (StudentID) REFERENCES Student(ID)
);

-- Create LabStudent Table
CREATE TABLE LabStudent(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
	,LabID INT NOT NULL
	,StudentID INT NOT NULL
	,Status VARCHAR(30)
	,FOREIGN KEY (LabID) REFERENCES Lab(ID)
	,FOREIGN KEY (StudentID) REFERENCES Student(ID)
);

-- Create Grade Table
CREATE TABLE Grade(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
	,SectionID INT NOT NULL
	,StudentID INT
	,Grade INT
	,FOREIGN KEY (SectionID) REFERENCES Section(ID)
	,FOREIGN KEY (StudentID) REFERENCES Student(ID)
);