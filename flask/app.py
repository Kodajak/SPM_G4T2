from sqlite3 import Cursor
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import mysql.connector as mysql
import requests
import json


app = Flask(__name__)
# enter your server IP address/domain name
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
# enter your code here!

cursor = db_connection.cursor()

CORS(app)

@app.route('/')
def home():
    return "Hello"

@app.route("/view_roles")
def view_Role():
    query = "SELECT * FROM Role"
    cursor.execute(query)
    roles = cursor.fetchall()
    return jsonify(
        {
            "data": dict(role for role in roles)
        }
    ), 200

@app.route("/view_ljRoles")
def view_LJRole ():
    query = "SELECT * FROM LJRole"
    cursor.execute(query)
    ljRoles = cursor.fetchall()
    return jsonify(
        {
            "data": ljRoles
        }
    ), 200

# to pull out the course id that is under skills
def getCourse(course_id):
    query = "SELECT course_name, course_desc FROM Course where course_id =" + str(course_id)
    cursor.execute(query)
    return cursor.fetchall()
# display it on html
@app.route("/view-course-skills/<int:skillID>")
def skill_by_course(skillID):

    query = "SELECT course_id FROM Course_Skill where skill_id =" + str(skillID)
    cursor.execute(query)
    courseUnderSkill = cursor.fetchall()
    courses = []
    for id in courseUnderSkill:
        courses.append(getCourse(id[0]))
    print(courses)
    
    return jsonify(
        {
            
            "data": courses
            # "data": {
            #     "courses": [course.json() for course in course_skills]
            # }
        }
    )

@app.route("/view_skills/<int:ljRole_Id>")
def view_skills(ljRole_Id):
    query = "SELECT LJR.ljrole_id, LJR.ljrole_name, LJR.ljrole_desc, All_skills.skill_id, All_skills.skill_desc, All_skills.Active FROM ((spmDB.LJRole LJR INNER JOIN spmDB.LJRole_Skill LJR_Skill ON LJR.ljrole_id = LJR_Skill.ljrole_id) INNER JOIN spmDB.Skill All_skills ON LJR_Skill.skill_id = All_skills.skill_id)"
    cursor.execute(query)
    skills = cursor.fetchall()
    filteredSkills = []
    for skill in skills:
        if skill[0] == ljRole_Id:
            filteredSkills.append([skill[3],skill[4], skill[5]])
    return jsonify(
        {
            "data": filteredSkills
        }
    ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
