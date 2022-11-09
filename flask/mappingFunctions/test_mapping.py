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
        query = "INSERT INTO Skill (skill_id, skill_name, skill_desc, status) VALUES (9999, 'Skill to Delete 2', 'Skill to Delete Description', 1)"
        cursor.execute(query)
        db_connection.commit()

        query = "INSERT INTO LJRole (ljrole_id, ljrole_name, ljrole_desc, status) VALUES (2222, 'LJRole to Delete', 'LJRole to Delete Description', 1)"
        cursor.execute(query)
        db_connection.commit()

        query = "INSERT INTO Course (course_id, course_name, course_desc, course_status, course_type, course_category) VALUES ('IS555', 'Course to Delete', 'Course to Delete Description', 'Active', 'Internal', 'course to delete category')"
        cursor.execute(query)
        db_connection.commit()

        query = "INSERT INTO LJRole_Skill (ljrole_id, skill_id) VALUES (2222, 9999)"
        cursor.execute(query)
        db_connection.commit()

        query = "INSERT INTO Course_Skill (course_id, skill_id) VALUES ('IS555', 9999)"
        cursor.execute(query)
        db_connection.commit()

        return super().setUp()
    
    def tearDown(self):
        query = "DELETE FROM Course_Skill WHERE skill_id = 9999"
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM LJRole_Skill WHERE ljrole_id = 2222"
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM LJRole WHERE ljrole_id = 2222"
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM Course WHERE course_id = 'IS555'"
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM Skill WHERE skill_id=9999"
        cursor.execute(query)
        db_connection.commit()

        return super().tearDown()

    def test_view_skill_mapping(self):
        r = requests.get('http://localhost:5000/view-skill-mapping/9999')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.encoding, 'utf-8')
        self.assertEqual(type(r.json()['skill']), list)
        self.assertEqual(type(r.json()['roles']), list)
        self.assertEqual(type(r.json()['courses']), list)

    def test_update_skill_mapping(self):
        r = requests.get("http://localhost:5000/update-skill-mapping/9999")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(type(r.json()['roles'][0]), list)
        self.assertEqual(type(r.json()['courses'][0]), list)
        self.assertEqual(r.json()['currentMappedCourses'][0][0], 'IS555')
        self.assertEqual(r.json()['currentMappedRoles'][0][0], 2222)

    def test_removeCourseMapping(self):
        r = requests.post("http://localhost:5000/removeCourseMapping/9999", json={
                "course": "IS555"
            })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "success")

    def test_removeRoleMapping(self):
        r = requests.post("http://localhost:5000/removeRoleMapping/9999", json={
                "role": 2222
            })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "success")

    def test_submit_mapping(self):
        query = "INSERT INTO LJRole (ljrole_id, ljrole_name, ljrole_desc, status) VALUES (2020, 'LJRole to POST', 'LJRole to POST Description', 1)"
        cursor.execute(query)
        db_connection.commit()

        query = "INSERT INTO Course (course_id, course_name, course_desc, course_status, course_type, course_category) VALUES ('ZZ555', 'Course to POST', 'Course to POST', 'Active', 'Internal', 'Course to POST category')"
        cursor.execute(query)
        db_connection.commit()

        r = requests.post("http://localhost:5000/submit-mapping/9999", json={
                "selectedRoles": [2020],
                "selectedCourses": ["ZZ555"],
                "currentMappedCourses": [["IS555", "Course to Delete", "Course to Delete Description" ,"Active","Internal", "course to delete category"]],
                "currentMappedRoles": [[2222, "LJRole to Delete", "LJRole to Delete Description", 1]]
            })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "success")
        # self.assertEqual(type(r.json()['roles'][0]), list)
        # self.assertEqual(type(r.json()['courses'][0]), list)
        # self.assertEqual(r.json()['currentMappedCourses'][0][0], 'IS555')
        # self.assertEqual(r.json()['currentMappedRoles'][0][0], 2222)

        query = "DELETE FROM spmDB.Course_Skill WHERE course_id = 'ZZ555'"
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM spmDB.LJRole_Skill WHERE ljrole_id = 2020"
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM spmDB.Course WHERE course_id = 'ZZ555'"
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM spmDB.LJRole WHERE ljrole_id = 2020"
        cursor.execute(query)
        db_connection.commit()
