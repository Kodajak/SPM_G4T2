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

class TestLJManagement(unittest.TestCase):
    def setUp(self):
       #add test staff_ID
        query = "INSERT INTO Staff (staff_id, staff_fname, staff_lname, dept, email, role_id) VALUES (%s, %s, %s,%s, %s, %s);"
        lj_data = (999999, 'first', 'last', 'test', 'test@mail.com', 2)
        cursor.execute(query, lj_data)
        db_connection.commit()

        return super().setUp()
    
    def tearDown(self):
       #add test staff_ID
        query = "DELETE FROM Staff WHERE staff_id = 999999"
        cursor.execute(query)
        db_connection.commit()

        return super().tearDown()

    def test_viewCoursesToAdd(self):
        ljID = 300002
        r = requests.get('http://localhost:5000/viewCoursesToAdd/' + str(ljID))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.encoding, 'utf-8')
        self.assertEqual(type(r.json()['data']), list)

    def test_addCoursesToLJ(self):
        query = "INSERT INTO LearningJourney (staff_id, ljrole_id, completion_status) VALUES (%s, %s, %s);"
        lj_data = (999999, 600005, 'Incomplete')
        cursor.execute(query, lj_data)
        db_connection.commit()

        query = "SELECT * FROM LearningJourney WHERE staff_id = %s AND ljrole_id = %s"
        details = (999999, 600005)
        cursor.execute(query, details)
        ljID = cursor.fetchall()[0][0]

        r2 = requests.post('http://localhost:5000/addCoursesToLj', json={
                        "selectedLj": ljID,
                        "selectedCourses": ['tch018', 'COR002'],
                    })
        self.assertEqual(r2.text, 'success')
        self.assertEqual(r2.status_code, 200)

        query = "DELETE FROM LJ_Course WHERE ljourney_id =" + str(ljID)
        cursor.execute(query)
        db_connection.commit()

        query = "DELETE FROM LearningJourney WHERE ljourney_id =" + str(ljID)
        cursor.execute(query)
        db_connection.commit()

    def test_removeLJCourses(self):
        query = "INSERT INTO LearningJourney (staff_id, ljrole_id, completion_status) VALUES (%s, %s, %s);"
        lj_data = (999999, 600005, 'Incomplete')
        cursor.execute(query, lj_data)
        db_connection.commit()

        query = "SELECT * FROM LearningJourney WHERE staff_id = %s AND ljrole_id = %s"
        details = (999999, 600005)
        cursor.execute(query, details)
        ljID = cursor.fetchall()[0][0]
        #add courses first
        requests.post('http://localhost:5000/addCoursesToLj', json={"selectedLj": ljID,"selectedCourses": ['tch018', 'COR002']})
        r =requests.post('http://localhost:5000/removeCoursesFromLj', json={"selectedLj": ljID,"selectedCourses": ['tch018', 'COR002']})
        self.assertEqual(r.text, 'course deletion success')
        self.assertEqual(r.status_code, 200)

        query = "DELETE FROM LearningJourney WHERE ljourney_id =" + str(ljID)
        cursor.execute(query)
        db_connection.commit()