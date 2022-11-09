-- Import Role Data
LOAD DATA INFILE  -- pathway of files provided. Do edit with your path.
"C:\Users\65907\OneDrive\Documents\SMU\Y3S1\Software Project Management IS212 G4\Project\RawData\Provided\role.csv"
INTO TABLE Role
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Import Staff Data
LOAD DATA INFILE  -- pathway of files provided. Do edit with your path.
"C:\Users\65907\OneDrive\Documents\SMU\Y3S1\Software Project Management IS212 G4\Project\RawData\Provided\staff.csv"
INTO TABLE Role
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Import LJRole Data
LOAD DATA INFILE  -- pathway of files provided. Do edit with your path.
"C:\Users\65907\OneDrive\Documents\SMU\Y3S1\Software Project Management IS212 G4\Project\RawData\Artificial\LJRole.csv"
INTO TABLE Role
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Import LearningJourney Data
LOAD DATA INFILE  -- pathway of files provided. Do edit with your path.
"C:\Users\65907\OneDrive\Documents\SMU\Y3S1\Software Project Management IS212 G4\Project\RawData\Artificial\LearningJourney.csv"
INTO TABLE Role
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Import Course Data
LOAD DATA INFILE  -- pathway of files provided. Do edit with your path.
"C:\Users\65907\OneDrive\Documents\SMU\Y3S1\Software Project Management IS212 G4\Project\RawData\Provided\course.csv"
INTO TABLE Role
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Import LJ_Course Data
LOAD DATA INFILE  -- pathway of files provided. Do edit with your path.
"C:\Users\65907\OneDrive\Documents\SMU\Y3S1\Software Project Management IS212 G4\Project\RawData\Artificial\LJ_Course.csv"
INTO TABLE Role
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Import Skill Data
LOAD DATA INFILE  -- pathway of files provided. Do edit with your path.
"C:\Users\65907\OneDrive\Documents\SMU\Y3S1\Software Project Management IS212 G4\Project\RawData\Artificial\Skill.csv"
INTO TABLE Role
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Import LJRole_Skill Data
LOAD DATA INFILE  -- pathway of files provided. Do edit with your path.
"C:\Users\65907\OneDrive\Documents\SMU\Y3S1\Software Project Management IS212 G4\Project\RawData\Artificial\LJRole_Skill.csv"
INTO TABLE Role
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Import Course_Skill Data
LOAD DATA INFILE  -- pathway of files provided. Do edit with your path.
"C:\Users\65907\OneDrive\Documents\SMU\Y3S1\Software Project Management IS212 G4\Project\RawData\Artificial\Course_Skill.csv"
INTO TABLE Course_Skill 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Import Registration Data
LOAD DATA INFILE  -- pathway of files provided. Do edit with your path.
"C:\Users\65907\OneDrive\Documents\SMU\Y3S1\Software Project Management IS212 G4\Project\RawData\Provided\registration.csv"
INTO TABLE Role
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;