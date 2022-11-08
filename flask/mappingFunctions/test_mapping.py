import pytest
import unittest
import requests
import mysql.connector as mysql

HOST = "database-1.cmqbhk3xoixj.ap-southeast-1.rds.amazonaws.com" # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "spmDB"
# "is212_example, spmDB"
# this is the user you create
USER = "admin"
# user password
PASSWORD = "spmspmspm"
# connect to MySQL server
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
print("Connected to:", db_connection.get_server_info())
cursor = db_connection.cursor()

class TestSkillMapping(unittest.TestCase):

    def setUp(self):

        return super().setUp()
    
    def tearDown(self):
        # query = 'DELETE FROM Skill WHERE skill_name="Skill to Delete 2"' 
        # cursor.execute(query)
        # db_connection.commit()

        # query = 'DELETE FROM Skill WHERE skill_name="Edited Skill Name"' 
        # cursor.execute(query)
        # db_connection.commit()

        # query = 'DELETE FROM Skill WHERE skill_name="skill"'
        # cursor.execute(query)
        # db_connection.commit()

        query = 'DELETE FROM Course WHERE course_name="Course to Delete"'
        cursor.execute(query)
        db_connection.commit()

        query = 'DELETE FROM LJRole WHERE ljrole_name="LJRole to Delete"'
        cursor.execute(query)
        db_connection.commit()

        return super().tearDown()

    def test_view_skill_mapping(self):
        query = "INSERT INTO Skill (skill_id, skill_name, skill_desc, status) VALUES (9999, 'Skill to Delete 2', 'Skill to Delete Description', 1)"
        cursor.execute(query)
        db_connection.commit()

        query = "INSERT INTO Course (course_id, course_name, course_desc, course_status, course_type, course_category) VALUES (1111, 'Course to Delete', 'Course to Delete Description', 'Active', 'Internal', 'course to delete category')"
        cursor.execute(query)
        db_connection.commit()

        query = "INSERT INTO Course_Skill (course_id, skill_id) VALUES (1111, 9999)"
        cursor.execute(query)
        db_connection.commit()

        query = "INSERT INTO LJRole (ljrole_id, ljrole_name, ljrole_desc, status) VALUES (2222, 'LJRole to Delete', 'LJRole to Delete Description', 1)"
        cursor.execute(query)
        db_connection.commit()

        query = "INSERT INTO LJRole_Skill (ljrole_id, skill_id) VALUES (2222, 9999)"
        cursor.execute(query)
        db_connection.commit()

        r = requests.get('http://localhost:5000/view-skill-mapping/9999')
        # Does this work?^^^ No skillID indicated
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.encoding, 'utf-8')
        self.assertEqual(type(r.json()['skill']), list)
        self.assertEqual(type(r.json()['roles']), list)
        self.assertEqual(type(r.json()['courses']), list)

        query = "DELETE FROM LJRole_Skill WHERE ljrole_id = 2222"
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM Course_Skill WHERE course_id = 1111"
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM LJRole WHERE ljrole_id = 2222"
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM Course WHERE course_id = 1111"
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM Skill WHERE skill_id=9999"
        cursor.execute(query)
        db_connection.commit()

    # def test_update_skill_mapping(self):
    #     r = requests.get("http://localhost:5000/update-skill-mapping/999999")
    #     self.assertEqual(r.status_code, 200)
    #     self.assertEqual(r.encoding, 'utf-8')
    #     self.assertEqual(type(r.json()['skill']), str)
    #     self.assertEqual(type(r.json()['roles']), list)
    #     self.assertEqual(type(r.json()['courses']), list)
    #     self.assertEqual(type(r.json()['currentMappedRoles']), list)
    #     self.assertEqual(type(r.json()['currentMappedCourses']), list)
