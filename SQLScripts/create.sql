-- Create Tables
-- CREATE LJRole Table
CREATE TABLE LJRole (
ljrole_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
ljrole_name VARCHAR(20) NULL,
ljrole_desc VARCHAR(255) NULL,
status BOOLEAN NOT NULL
);
-- Create Role Table 
CREATE TABLE Role (
role_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
role_name VARCHAR(20) NOT NULL
);
-- Create Staff Table
CREATE TABLE Staff (
staff_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
staff_fname VARCHAR(50) NOT NULL,
staff_lname VARCHAR(50) NOT NULL,
dept VARCHAR(50) NOT NULL,
email VARCHAR(50) NOT NULL,
role_id INT NOT NULL,
CONSTRAINT staff_fk FOREIGN KEY (role_id) references Role(role_id)
);
-- Create LearningJourney Table
CREATE TABLE LearningJourney (
ljourney_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
staff_id INT NOT NULL,
ljrole_id INT NOT NULL,
completion_status VARCHAR(255) NOT NULL,
CONSTRAINT learningjourney_fk1 FOREIGN KEY (staff_id) references Staff(staff_id),
CONSTRAINT learningjourney_fk2 FOREIGN KEY (ljrole_id) references LJRole(ljrole_id)
);
-- Create Course Table
CREATE TABLE Course (
course_id VARCHAR(20) NOT NULL PRIMARY KEY,
course_name VARCHAR(50) NOT NULL,
course_desc VARCHAR(255) NULL,
course_status VARCHAR(15) NULL,
course_type VARCHAR(10) NULL,
course_category VARCHAR(50) NULL
);
-- Create LJ_Course Associative Entity
CREATE TABLE LJ_Course (
ljourney_id INT NOT NULL,
course_id VARCHAR(20) NOT NULL,
CONSTRAINT ljourney_course_fk FOREIGN KEY (ljourney_id) references LearningJourney(ljourney_id),
CONSTRAINT ljourney_course_fk2 FOREIGN KEY (course_id) references Course(course_id)
);
-- Create Skill
CREATE TABLE Skill (
skill_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
skill_name VARCHAR(100) NOT NULL,
skill_desc VARCHAR(255) NOT NULL,
status BOOLEAN NOT NULL
);
-- Create Course_Skill Associative Entity
CREATE TABLE Course_Skill (
course_id VARCHAR(20) NOT NULL,
skill_id INT NOT NULL,
CONSTRAINT course_skill_fk FOREIGN KEY (course_id) references Course(course_id),
CONSTRAINT course_skill_fk2 FOREIGN KEY (skill_id) references Skill(skill_id)
);
-- Create LJRole_Skill Associative Entity
CREATE TABLE LJRole_Skill (
ljrole_id INT NOT NULL,
skill_id INT NOT NULL,
CONSTRAINT ljrole_skill_fk FOREIGN KEY (ljrole_id) references LJRole(ljrole_id),
CONSTRAINT ljrole_skill_fk2 FOREIGN KEY (skill_id) references Skill(skill_id)
);
-- Create Registration
CREATE TABLE Registration (
reg_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
course_id VARCHAR(20) NOT NULL,
staff_id INT NOT NULL,
reg_status VARCHAR(20) NOT NULL,
completion_status VARCHAR(20) NOT NULL,
CONSTRAINT registration_fk FOREIGN KEY (course_id) references Course(course_id),
CONSTRAINT registration_fk2 FOREIGN KEY (staff_id) references Staff(staff_id)
);

-- Check Populated Tables
-- Fact Entities
SELECT * from Role;
SELECT * from Staff;
SELECT * from LearningJourney;
SELECT * from LJRole;
SELECT * from Course;
SELECT * from Skill;
SELECT * from Registration;
-- Associative Entities
SELECT * from LJ_Course;
SELECT * from LJRole_Skill;
SELECT * from Course_Skill;

-- Update Data Template
UPDATE LJRole
SET status = true;
UPDATE Skill
SET status = true;

-- Delete Data Template
-- DELETE FROM LJ_Course WHERE ljourney_id = 300008;
-- DELETE FROM LearningJourney WHERE ljourney_id IN (300007, 300008, 300009);