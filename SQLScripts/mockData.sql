-- Used Before Mock Data in Minutes came out

-- Mock Data Population
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
(467467,'Sales Lead', 'Leads a Sales team.', true),
(555999,'HR Lead','Heads a HR team.', true),
(675848,'Senior Software Engineer','Advice the team with minimal coding.', true),
(777777,'Managing Director','Align the company.', true),
(957685,'Sales Executive','Senior Sales.', true);
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
(528691,'Advanced Domain Knowledge', true),
(653756,'Advanced People Skills', true),
(997453,'Professional Progamming Practices', true),
(234234,'Professional People Skills', true),
(870342,'Professional Domain Knowledge', true),
(178234,'Professional Communication Skills', true),
(794236,'Intermediate Domain Knowledge', true);
-- Populate Course
INSERT INTO Course
VALUES 
(884453,'Domain Knowledge III', 'In-depth Learning of Domain Knowledge', 'Active', 'Graded', 'General'),
(197354,'People Skills III', 'Effective Communication and Interpersonal Skills', 'Active', 'Ungraded', 'General'),
(664752,'Progamming Practices IV', 'Able to teach and understand various coding styles', 'Active', 'Graded', 'Programming'),
(528631,'People Skills IV', 'Global Relationship Handling', 'Active', 'Ungraded', 'General'),
(495328,'Domain Knowledge IV', 'Able to teach domain knowledge', 'Active', 'Graded', 'General'),
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
(554986,794236),
(197354,870342);