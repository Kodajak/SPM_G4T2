-- Create Tables
-- CREATE LJRole Table
CREATE TABLE LJRole (
ljrole_id INT NOT NULL PRIMARY KEY,
ljrole_name VARCHAR(20) NULL,
ljrole_desc VARCHAR(255) NULL
);
-- Create LearningJourney Table
CREATE TABLE LearningJourney (
ljourney_id INT NOT NULL PRIMARY KEY,
ljrole_id INT NOT NULL,
completion_status VARCHAR(255) NOT NULL,
CONSTRAINT learningjourney FOREIGN KEY (ljrole_id) references LJRole(ljrole_id)
);
-- Create Role Table 
CREATE TABLE Role (
role_id INT NOT NULL PRIMARY KEY,
role_name VARCHAR(20) NOT NULL
);
-- Create Staff Table
CREATE TABLE Staff (
staff_id INT NOT NULL PRIMARY KEY,
staff_fname VARCHAR(50) NOT NULL,
staff_lname VARCHAR(50) NOT NULL,
dept VARCHAR(50) NOT NULL,
email VARCHAR(50) NOT NULL,
ljourney_id INT NOT NULL,
CONSTRAINT staff_fk FOREIGN KEY (ljourney_id) references LearningJourney(ljourney_id)
);
-- Create Staff_Role Associative Entity
CREATE TABLE Staff_Role (
staff_id INT NOT NULL,
role_id INT NOT NULL,
CONSTRAINT staff_role_fk FOREIGN KEY (staff_id) references Staff(staff_id),
CONSTRAINT staff_role_fk2 FOREIGN KEY (role_id) references Role(role_id)
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
-- Create LJourney_Course Associative Entity
CREATE TABLE LJourney_Course (
ljourney_id INT NOT NULL,
course_id VARCHAR(20) NOT NULL,
CONSTRAINT ljourney_course_fk FOREIGN KEY (ljourney_id) references LearningJourney(ljourney_id),
CONSTRAINT ljourney_course_fk2 FOREIGN KEY (course_id) references Course(course_id)
);
CREATE TABLE Skill (
skill_id INT NOT NULL PRIMARY KEY,
skill_desc VARCHAR(255) NOT NULL
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

-- Populate Tables
-- Populate Role
INSERT INTO Role
VALUES 
(001,'Admin'),
(002,'Manager'),
(003,'User');
-- Populate Staff
INSERT INTO Staff
VALUES
(123456,'John','Snow','Sales','johnsnow@smoo.com',654321),
(123457,'Esther','Rain','HR','estherrain@smoo.com',239826),
(123458,'Phil','Son','Tech','philson@smoo.com',999111),
(123459,'Ben','Dover','HR','bendover@smoo.com',666999),
(123460,'Rachel','Green','Sales','rachelgreen@smoo.com',873922);
-- Populate Staff_Role
INSERT INTO Staff_Role
VALUES 
(123456,002),
(123456,003),
(123457,001),
(123457,003),
(123458,003),
(123459,001),
(123459,003),
(123460,003);
-- Populate LearningJourney
INSERT INTO LearningJourney
VALUES
(654321,467467, 'Partial'),
(239826,555999,'Partial'),
(999111,675848,'Not Started'),
(666999,777777,'Completed'),
(873922,957685,'Partial');
-- Populate LJRole
INSERT INTO LJRole
VALUES
(467467,'Sales Lead', 'Leads a Sales team.'),
(555999,'HR Lead','Heads a HR team.'),
(675848,'Senior Software Engineer','Advice the team with minimal coding.'),
(777777,'Managing Director','Align the company.'),
(957685,'Sales Executive','Senior Sales.');
select * from LJRole;
-- Populate LJRole_Skill
INSERT INTO LJRole_Skill
VALUES 
(467467,528691),
(555999,653756),
(675848,997453),
(777777,234234),
(777777,870342),
(777777,178234),
(957685,794236);
-- Populate Skill
INSERT INTO Skill
VALUES 
(528691,'Advanced Domain Knowledge'),
(653756,'Advanced People Skills'),
(997453,'Professional Progamming Practices'),
(234234,'Professional People Skills'),
(870342,'Professional Domain Knowledge'),
(178234,'Professional Communication Skills'),
(794236,'Intermediate Domain Knowledge');
-- Populate Course
INSERT INTO Course
VALUES 
(884453,'Domain Knowledge III', 'In-depth Learning of Domain Knowledge', 'Active', 'Graded', 'General'),
(197354,'People Skills III', 'Effective Communication and Interpersonal Skills', 'Active', 'Ungraded', 'General'),
(664752,'Progamming Practices IV', 'Able to teach and understand various coding styles', 'Active', 'Graded', 'Programming'),
(528631,'People Skills IV', 'Global Relationship Handling', 'Active', 'Ungraded', 'General'),
(495328,'Domain Knowledge IV', 'Able to teach domain know', 'Active', 'Graded', 'General'),
-- (494237,'Communication Skills IV', 'Able to communicate effectively with stakeholders', 'Active', 'Ungraded', 'General'),
(554986,'Domain Knowledge II', 'Increased Learning of Domain Knowledge', 'Active', 'Graded', 'General');
-- Populate LJourney_Course
INSERT INTO LJourney_Course
VALUES 
(654321,884453),
(239826,197354),
(239826,664752),
(666999,528631),
(666999,495328),
(873922,554986);
-- Populate Course_Skill
INSERT INTO Course_Skill
VALUES
(884453,528691),
(197354,653756),
(664752,997453),
(528631,234234),
(495328,870342),
(528631,178234),
(554986,794236);

-- Alter Table
-- Alter LJRole
ALTER TABLE LJRole
ADD Active boolean not null;
-- Alter Skill
ALTER TABLE Skill
ADD Active boolean not null;

SELECT * 
FROM LJRole;
SELECT * 
FROM Skill;

ALTER TABLE LJRole
MODIFY Active boolean;