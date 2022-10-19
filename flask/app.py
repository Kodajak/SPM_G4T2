from sqlite3 import Cursor
from urllib import response
from flask import Flask, request, jsonify, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import mysql.connector as mysql
import json

import requests

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

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = '/Applications/MAMP/htdocs/SPMProject/SPM%20Project/csv/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return ""

def parseCSV(filePath):
   # CVS Column Names
    col_names = ['Course_ID', 'Course_Name', 'Course_Desc', 'Course_Status', 'Course_Type', 'Course_Category']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names = col_names, header = None, encoding= 'unicode_escape', skiprows=1)
    # Loop through the Rows
    for i, row in csvData.iterrows():
        sql = "INSERT INTO Course_Test (Course_ID, Course_Name, Course_Desc, Course_Status, Course_Type, Course_Category) VALUES (%s, %s, %s, %s, %s, %s)"
        value = (row['Course_ID'], row['Course_Name'], row['Course_Desc'], row['Course_Status'], row['Course_Type'], row['Course_Category'])
        cursor.execute(sql, value)
        db_connection.commit()
        print(value)

@app.route("/import_csv", methods=['POST'])
def uploadFiles():
   # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # set the file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    # save the file
    uploaded_file.save(file_path)
    
    parseCSV(file_path)
    return redirect(('http://localhost:8888/SPMProject/SPM%2520Project/htdocs/coursesManagement.html'))

@app.route("/view_roles")
def view_Role():
    query = "SELECT * FROM Role"
    cursor.execute(query)
    roles = cursor.fetchall()
    return jsonify(
        {
            "data": dict(role for role in roles)
        }
    )

@app.route("/view_ljRoles")
def view_LJRole ():
    query = "SELECT * FROM LJRole"
    cursor.execute(query)
    ljRoles = cursor.fetchall()
    return jsonify(
        {
            "data": ljRoles
        }
    )

@app.route("/create_ljRoles", methods=['POST'])

def create_LJRole():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        role = data['data'][0]
        desc = data['data'][1]

        query2 = "INSERT INTO LJRole (ljrole_name, ljrole_desc) VALUES (%s, %s)"
        val = (role,desc)
        cursor.execute(query2, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return role

# to pull out the course id that is under skills
def getCourseByID(course_id):
    query = "SELECT DISTINCT * FROM Course WHERE course_status='Active'" + "AND course_id ='" + str(course_id)+"'"
    cursor.execute(query)
    return cursor.fetchall()
    
# display course under skills on html
@app.route("/view-course-skills/<int:skillID>")
def skill_by_course(skillID):

    query = "SELECT course_id FROM Course_Skill WHERE skill_id =" + str(skillID)
    cursor.execute(query)
    courseUnderSkill = cursor.fetchall()

    query = "SELECT skill_desc FROM Skill WHERE skill_id =" + str(skillID)
    cursor.execute(query)
    skill = cursor.fetchall()
    print(skill)
    courses = []
    for id in courseUnderSkill:
        courses.append(getCourseByID(id[0]))
    print(courses)
    
    return jsonify(
        {
            "data": courses,
            "skill":skill
        }
    )

# display list of courses
@app.route("/view-course-list")
def courses():
    query = "SELECT * FROM Course_Test"
    cursor.execute(query)
    courseUnderSkill = cursor.fetchall()
    return jsonify(
        {
            "data": courseUnderSkill
        }
    )

# display list of skills
@app.route("/view-skills")
def skills():
    query = "SELECT * FROM Skill"
    cursor.execute(query)
    skills = cursor.fetchall()
    return jsonify(
        {
            "data": skills
        }
    )

# display skill mapping of roles and courses
@app.route("/view-skill-mapping/<int:skillID>")
def skill_mapping(skillID):
    query = f"SELECT * FROM Skill WHERE skill_id = {skillID}" 
    cursor.execute(query)
    skill = cursor.fetchall()
    
    queryC = f"SELECT * " \
    "FROM Course " \
    "WHERE course_id IN (SELECT DISTINCT courseid from (SELECT DISTINCT c.course_id as courseid " \
	"FROM Skill s, Course_Skill c " \
    "WHERE s.skill_id = c.skill_id " \
	f"AND s.skill_id = {skillID}) as RCS);"
    cursor.execute(queryC)
    courseUnderSkill = cursor.fetchall()

    queryR = f"SELECT * "\
    "FROM LJRole "\
    "WHERE ljrole_id IN (SELECT DISTINCT roleid from (SELECT DISTINCT r.ljrole_id as roleid "\
	"FROM Skill s, LJRole_Skill r, Course_Skill c " \
	"WHERE s.skill_id = r.skill_id " \
	f"AND s.skill_id = {skillID}) as RCS);" 
    cursor.execute(queryR)
    roleUnderSkill = cursor.fetchall()

    return jsonify(
        {
            "skill" : skill,
            "roles": roleUnderSkill,
            "courses": courseUnderSkill
        }
    )

# show skill mapping of roles and courses
@app.route("/update-skill-mapping/<int:skillID>")
def update_skill_mapping(skillID):
    
    view_Role()
    courses()
    courseList = requests.get("http://0.0.0.0:5000/view-course-list")
    courseList.raise_for_status()
    jsoncourseList = courseList.json()
    # rename key in dictionary
    jsoncourseList["courses"] = jsoncourseList.pop("data") 
    print(jsoncourseList)

    skill = "SELECT * FROM Skill WHERE skill_id="+str(skillID)
    cursor.execute(skill)
    skill = cursor.fetchall()
    print(skill)

    roleList = requests.get("http://0.0.0.0:5000/view_ljRoles")
    roleList.raise_for_status()
    jsonroleList = roleList.json()
    # rename key in dictionary
    jsonroleList["roles"] = jsonroleList.pop("data") 
    print(jsonroleList)

    csr = {}
    
    csr.update(jsonroleList)
    csr.update(jsoncourseList)
    return jsonify(
        {
            "skill" : skill,
            "roles": csr['roles'],
            "courses": csr['courses']
        }
    )
# create skill mapping
@app.route("/submit-mapping/<int:skillID>", methods=["POST"])
def submit_mapping(skillID):
    # check for missing inputs
    data = request.get_json()
    print(data)
    if not all(key in data.keys() for
               key in ('selectedRoles', 'selectedCourses')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
  
    # if form validation succesful
    try:
        selectedRoles = data['selectedRoles']
        print(selectedRoles)
        for role in selectedRoles:
            query = "INSERT INTO LJRole_Skill (ljrole_id, skill_id) VALUES (%s, %s);"

            ljrole_skill_data = (role, skillID)
            cursor.execute(query, ljrole_skill_data)
            db_connection.commit()
            print("pass")

        checking = "SELECT * FROM LJRole_Skill;"
        cursor.execute(checking)
        print(cursor.fetchall())

        selectedCourses = data['selectedCourses']
        print(selectedCourses)

        for course in selectedCourses:
            query2 = "INSERT INTO Course_Skill(course_id, skill_id) VALUES (%s,%s);"
            course_skill_data = (course, skillID)
            cursor.execute(query2, course_skill_data)
            db_connection.commit()
            print("pass")
        print("completed")

        checking = "SELECT * FROM Course_Skill"
        cursor.execute(checking)
        print(cursor.fetchall())
        return jsonify("success"), 201

    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

# get skills based on selected ljRole id
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

# get new learning journey ID
def getLjId():
    query = "SELECT MAX(ljourney_id) FROM LearningJourney"
    cursor.execute(query)
    data = cursor.fetchall()
    id = data[0][0]
    return id

@app.route("/create_lj", methods=["POST"])
def create_lj():
    # check for missing inputs
    data = request.get_json()
    print(data)
    if not all(key in data.keys() for
               key in ('selectedRole', 'selectedCourses')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
  
    # if form validation succesful
    try:
    # sample_query = "SELECT ljrole_id FROM LearningJourney"
    # cursor.execute(sample_query)
    # id = cursor.fetchall()
    # print(id)
    # count = len(id) + 1
    # print(count)
    # sampleRoleId = 22
    # completionStatus = 'Incomplete'

        selectedRole = data['selectedRole']
        print(selectedRole)
        print(type(selectedRole))
        query = "INSERT INTO LearningJourney (ljrole_id, completion_status) VALUES (%s, %s);"

        lj_data = (selectedRole[0], 'Incomplete')
        cursor.execute(query, lj_data)
        db_connection.commit()
        print("pass 1")

        sample_query = "SELECT * FROM LearningJourney"
        cursor.execute(sample_query)
        print(cursor.fetchall())

        # get new learning journey Id
        newLjId = getLjId()

        print(newLjId)
        selectedCourses = data['selectedCourses']
        for course in selectedCourses:
            print(course[0])
            query2 = "INSERT INTO LJourney_Course VALUES (" + str(newLjId) + ","+ str(course[0]) + ")"
            cursor.execute(query2)
            db_connection.commit()
        print("completed")

        sample_query2 = "SELECT * FROM LJourney_Course"
        cursor.execute(sample_query2)
        print(cursor.fetchall())
        return jsonify("success"), 201

    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
