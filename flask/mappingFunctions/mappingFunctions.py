from flask import Flask, request, jsonify, request, Blueprint
from flask_cors import CORS
import mysql.connector as mysql
import requests

mappingFunctions = Blueprint('mappingFunctions', __name__)

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

CORS(mappingFunctions)

# [START] Function to GET skill mapping of roles and courses based on a specified skill ID
@mappingFunctions.route("/view-skill-mapping/<int:skillID>")
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
# [END] Function to GET skill mapping of roles and courses based on a specified skill ID

# [START] Function to GET skill mapping of roles name and course names based on a specified skill ID
@mappingFunctions.route("/update-skill-mapping/<int:skillID>")
def update_skill_mapping(skillID):
    courseList = requests.get("http://0.0.0.0:5000/view-course-list")
    courseList.raise_for_status()
    jsoncourseList = courseList.json()
    # rename key in dictionary
    jsoncourseList["courses"] = jsoncourseList.pop("courses")

    skill = "SELECT * FROM Skill WHERE skill_id="+str(skillID)
    cursor.execute(skill)
    skill = cursor.fetchall()

    roleList = requests.get("http://0.0.0.0:5000/view_ljRoles")
    roleList.raise_for_status()
    jsonroleList = roleList.json()
    # rename key in dictionary
    jsonroleList["roles"] = jsonroleList.pop("data")

    query = "SELECT lr.ljrole_id, lr.ljrole_name FROM LJRole_Skill lrs, LJRole lr WHERE lrs.ljrole_id = lr.ljrole_id  AND skill_id =" + str(skillID)
    cursor.execute(query)
    currentMappedRoles = cursor.fetchall()

    currentMapped = requests.get("http://0.0.0.0:5000/view-skill-mapping/"+str(skillID))
    currentMapped.raise_for_status()
    cm = currentMapped.json()

    csr = {}

    csr.update(jsonroleList)
    csr.update(jsoncourseList)

    for x in cm['courses']:
        for y in  csr['courses']:
            if(x[0] == y[0]):
                csr['courses'].remove(y)

    for x in cm['roles']:
        for y in  csr['roles']:
            if(x[0] == y[0]):
                csr['roles'].remove(y)

    return jsonify(
        {
            "skill" : skill,
            "roles": csr['roles'],
            "courses": csr['courses'],
            "currentMappedRoles": cm['roles'],
            "currentMappedCourses": cm['courses']
        }
    )
# [END] Function to GET skill mapping of roles name and course names based on a specified skill ID

# [START] Function to DELETE skill mapping of course  based on a specified skill ID
@mappingFunctions.route("/removeCourseMapping/<int:skillID>", methods=["POST"])
def removeCourseMapping(skillID):
    # check for missing inputs
    data = request.get_json()

    try:
        course = data['course']
        query = "DELETE FROM Course_Skill WHERE skill_id = (%s) AND course_id= (%s)"
        course_data = (str(skillID), str(course))
        cursor.execute(query, course_data)
        db_connection.commit()
        print(course_data)
        return jsonify("success"), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500
# [END] Function to DELETE skill mapping of course  based on a specified skill ID

# [START] Function to DELETE skill mapping of role  based on a specified skill ID
@mappingFunctions.route("/removeRoleMapping/<int:skillID>", methods=["POST"])
def removeRoleMapping(skillID):
    # check for missing inputs
    data = request.get_json()
    print(data['role'])
    try:
        role = data['role']
        query = "DELETE FROM LJRole_Skill WHERE skill_id = (%s) AND ljrole_id = (%s)"
        role_data = (str(skillID), str(role))
        cursor.execute(query, role_data)
        db_connection.commit()
        print(role_data)
        return jsonify("success"), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500
# [END] Function to DELETE skill mapping of role  based on a specified skill ID

# [START] Function to ADD/UPDATE skill mapping of roles name and course names based on a specified skill ID
@mappingFunctions.route("/submit-mapping/<int:skillID>", methods=["POST"])
def submit_mapping(skillID):
    # check for missing inputs
    data = request.get_json()
    if not all(key in data.keys() for
               key in ('selectedRoles', 'selectedCourses', 'currentMappedCourses','currentMappedRoles')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500

    # if form validation succesful
    try:

        selectedRoles = []
        selectedCourses = []

        query = "DELETE FROM LJRole_Skill WHERE skill_id = " + str(skillID) + ";"
        query2 = "DELETE FROM Course_Skill WHERE skill_id = " + str(skillID) + ";"
        cursor.execute(query)
        db_connection.commit()

        cursor.execute(query2)
        db_connection.commit()

        for rid in data['currentMappedRoles']:
            selectedRoles.append(rid[0])
        for rid in data['selectedRoles']:
            selectedRoles.append(rid)

        for role in selectedRoles:
            query = "INSERT INTO LJRole_Skill (ljrole_id, skill_id) VALUES (%s, %s);"
            ljrole_skill_data = (role, skillID)
            cursor.execute(query, ljrole_skill_data)
            db_connection.commit()
            print('pass')

        for cid in data['currentMappedCourses']:
            selectedCourses.append(cid[0])
        for cid in data['selectedCourses']:
            selectedCourses.append(cid)

        for course in selectedCourses:
            query2 = "INSERT INTO Course_Skill(course_id, skill_id) VALUES (%s,%s);"
            course_skill_data = (course, skillID)
            cursor.execute(query2, course_skill_data)
            db_connection.commit()
            print('pass')



        return jsonify("success"), 201

    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500
# [END] Function to ADD/UPDATE skill mapping of roles name and course names based on a specified skill ID

# --------- Mapping Functions ---------
# -------------------- END --------------------