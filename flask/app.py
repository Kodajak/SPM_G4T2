from flask import Flask, request, jsonify, request, redirect
import os
import pandas as pd
from flask_cors import CORS
import mysql.connector as mysql
import json
import requests

app = Flask(__name__, template_folder='../htdocs')
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

# --------- Skills Management Functions ---------
# -------------------- Start --------------------

# [START] Function to GET ALL skills
@app.route("/view_Skills")
def view_allSkills ():
    query = "SELECT * FROM Skill"
    cursor.execute(query)
    allSkills = cursor.fetchall()
    return jsonify(
        {
            "data": allSkills
        }
    ), 200
# [START] Function to GET ALL skills details

# [START] Function to GET ALL Course ID linked to Skill ID
@app.route("/get_CourseSkill")
def get_CourseSkill():
    query = "SELECT * FROM Course_Skill"
    cursor.execute(query)
    courseSkill = cursor.fetchall()
    return jsonify(
        {
            "data": courseSkill
        }
    ), 200
# [END] Function to GET ALL Course ID linked to Skill ID

# [START] Function to GET ALL learning journey role ID linked to Skill ID
@app.route("/get_RoleSkill")
def get_RoleSkill():
    query = "SELECT * FROM LJRole_Skill"
    cursor.execute(query)
    roleSkill = cursor.fetchall()
    return jsonify(
        {
            "data": roleSkill
        }
    ), 200
# [END] Function to GET ALL learning journey role ID linked to Skill ID

# [START] Function to CREATE a skill
@app.route("/create_Skill", methods=['POST'])
def create_Skills():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        skillName = data['data'][0]
        skillDesc = data['data'][1]

        query2 = "INSERT INTO Skill (skill_name, skill_desc, status) VALUES (%s, %s, %s)"
        val = (skillName, skillDesc, 1)
        cursor.execute(query2, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return skillName + ' saved'
# [END] Function to CREATE a skill

# [START] Function to DELETE a skill based on sepcified skill ID
@app.route("/delete_Skill/<int:id>", methods=['DELETE'])
def delete_Skill(id):
    response_object = {'status': 'success'}
    id = str(id)
    if (request.method=='DELETE'):
        query = "DELETE FROM Skill WHERE skill_id =" + id 
        cursor.execute(query)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'skill ' + id + ' deleted'
# [END] Function to DELETE a skill based on sepcified skill ID

# [START] Function to SOFT DELETE a skill based on sepcified skill ID
@app.route("/switchStatus/<int:id>", methods=['POST'])
def switchStatus(id):
    response_object = {'status': 'success'}
    id = str(id)
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        if (data['data'][0] == 0):
            query = "UPDATE Skill SET status=0 WHERE skill_id=" + id
        else:
            query = "UPDATE Skill SET status=1 WHERE skill_id=" + id

        cursor.execute(query)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'skill ' + id + ' switched to ' + str(data['data'][0])
# [END] Function to SOFT DELETE a skill based on sepcified skill ID

# [START] Function to EDIT a skill based on sepcified skill ID
@app.route("/edit_Skill", methods=['GET', 'POST'])
def edit_Skill():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        skill_name = data['data'][1]
        skill_desc = data['data'][2]
        skill_id = str(data['data'][0])

        query = "UPDATE Skill SET skill_name=%s, skill_desc=%s WHERE skill_id=%s"
        val = (skill_name, skill_desc, skill_id)
        cursor.execute(query, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'skill ' + str(skill_id) + ' edited'
# [END] Function to EDIT a skill based on sepcified skill ID

# -------- Skills Management Functions --------
# -------------------- End --------------------


# --------- Roles Management Functions ---------
# -------------------- Start --------------------

# [START] Function to GET ALL learning journey roles
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
# [END] Function to GET ALL learning journey roles

# [START] Function to SOFT DELETE a learning journey role based on a specified learning journey role ID
@app.route("/softDelete_ljrole", methods=['POST'])
def softDelete_role():
    response_object = {'status': 'success'}
    if (request.method=='POST'):
        data = request.get_json()
        id = str(data['data'][0][0])
        stat = data['data'][0][3]
        if(stat==1):
            stat=0
        else:
            stat=1
        query = "UPDATE LJRole SET status="+str(stat)+" WHERE ljrole_id= " + id
        cursor.execute(query)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'ljrole' + id + ' status changed'
# [END] Function to SOFT DELETE a learning journey role based on a specified learning journey role ID

# [START] Function to EDIT a learning journey role based on a specified learning journey role ID
@app.route("/edit_Role", methods=['GET', 'POST'])
def edit_Role():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        role_name = data['data'][0][1]
        role_desc = data['data'][0][2]
        role_id = str(data['data'][0][0])

        query = "UPDATE LJRole SET ljrole_name=%s, ljrole_desc=%s WHERE ljrole_id=%s"
        val = (role_name, role_desc, role_id)
        cursor.execute(query, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'role ' + str(role_id) + ' edited'
# [END] Function to EDIT a learning journey role based on a specified learning journey role ID

# [START] Function to CREATE a learning journey role based on a specified learning journey role ID
@app.route("/create_ljRoles", methods=['POST'])
def create_LJRole():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        role = data['data'][0]
        desc = data['data'][1]

        query2 = "INSERT INTO LJRole (ljrole_name, ljrole_desc, status) VALUES (%s, %s,%s)"
        val = (role,desc,1)
        cursor.execute(query2, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return role
# [END] Function to CREATE a learning journey role based on a specified learning journey role ID

# --------- Roles Management Functions ---------
# -------------------- End ---------------------

# --------- Course Management Functions ---------
# -------------------- Start --------------------

# [START] Function to convert CSV file to insert data into Database
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
# [END] Function to convert CSV file to insert data into Database
    
# [START] Function to IMPORT all courses from CSV file
@app.route("/import_csv", methods=['POST'])
def uploadFiles():
   # get the uploaded file
    if('file' in request.files):
        uploaded_file = request.files['file']
        if uploaded_file.filename == 'courses.csv':
            # set the file path
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # save the file
            uploaded_file.save(file_path)
            try:
                parseCSV(file_path)
                msg = {"msg":"Successfully imported courses !"}
                return jsonify(msg)
            except mysql.errors.IntegrityError:
                msg = {"msg": "Duplicated courses found ! Import Fail !"}
                return jsonify(msg)
            except Exception:
                msg = {"msg": "Unable to commit to database !"}
                return jsonify(msg)
        else:
            msg = {"msg": "Import only course.csv !"}
            return jsonify(msg)
    else:
        return ({
            "msg": ""
        })
# [END] Function to IMPORT all courses from CSV file

# [START] Function to GET all courses 
@app.route("/view-course-list")
def courses():
    query = "SELECT * FROM Course"
    cursor.execute(query)
    courseUnderSkill = cursor.fetchall()
    
    return jsonify(
        {
            "courses": courseUnderSkill
        }
    )
# [END] Function to GET all courses 

# --------- Course Management Functions ---------
# -------------------- END --------------------

# [START] Function to GET active courses based on specified course ID
def getCourseByID(course_id):
    query = "SELECT DISTINCT * FROM Course WHERE course_status='Active'" + "AND course_id ='" + str(course_id)+"'"
    cursor.execute(query)
    return cursor.fetchall()
# [END] Function to GET active courses based on specified course ID

# [START] Function to GET courses ID bsed on a specific skill ID
def get_course_by_skillId(skillId):
        query = "SELECT course_id FROM Course_Skill WHERE skill_id=" + str(skillId)
        cursor.execute(query)
        return cursor.fetchall()    
# [END] Function to GET courses ID based on a specific skill ID

# [START] Function to GET skill description and courses based on a specified skill ID
@app.route("/view-course-skills/<int:skillID>")
def skill_by_course(skillID):
    courseUnderSkill = get_course_by_skillId(skillID)
    query = "SELECT skill_desc FROM Skill WHERE skill_id =" + str(skillID)
    cursor.execute(query)
    skill = cursor.fetchall()
    print(courseUnderSkill)
    courses = []
    for id in courseUnderSkill:
        # check if function returns empty list
        if getCourseByID(id[0]) != []:
            courses.append(getCourseByID(id[0]))
    return jsonify(
        {
            "data": courses,
            "skill":skill
        }
    )
# [END] Function to GET courses based on a specified skill ID

# [START] Function to GET skill mapping of roles and courses based on a specified skill ID
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
# [END] Function to GET skill mapping of roles and courses based on a specified skill ID

# [START] Function to GET skill mapping of roles name and course names based on a specified skill ID
@app.route("/update-skill-mapping/<int:skillID>")
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

# [START] Function to ADD/DELETE/UPDATE skill mapping of roles name and course names based on a specified skill ID
@app.route("/submit-mapping/<int:skillID>", methods=["POST"])
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
# [END] Function to ADD/DELETE/UPDATE skill mapping of roles name and course names based on a specified skill ID
# [START] Function to GET all skills 
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
# [END] Function to GET all skills 

# --------- Skill Management Functions ---------
# -------------------- END --------------------

# --------- Staff Learning Journey Creation Functions ---------
# --------------------------- Start ---------------------------
# [START] Function to GET all skills based on specified Learning Journey role ID
@app.route("/view_skills/<int:ljRole_Id>")
def view_skills(ljRole_Id):
    # get relevant skills ID matched with roleId
    skillsId = get_skills_id(ljRole_Id)
    
    skillsIdQuery = "("
    for item in skillsId:
        skillsIdQuery += str(item[0]) + ","
    skillsIdQuery = skillsIdQuery[:-1]
    skillsIdQuery += ")"
    # get skills that match skills id retrieved earlier and are active 
    query = "SELECT * FROM Skill WHERE skill_id in" + str(skillsIdQuery)
    cursor.execute(query)
    skills = cursor.fetchall()
    return jsonify(
        {
            "data": skills
        }
    ), 200
# [END] Function to GET all skills based on specified Learning Journey role ID

# [START] Function to get staff learning journey
def get_all_staff_lj(staffId):
    query = "SELECT * FROM LearningJourney WHERE staff_id=" + str(staffId)
    cursor.execute(query)
    return cursor.fetchall()
# [END] Function to get staff learning journey

# [START] Function to GET nested list of Unselected and Selected active roles
@app.route("/view_filteredLjRoles/<int:staffId>")
def view_filteredRoles(staffId):
    data = get_all_staff_lj(staffId)
    existingRoleId = []
    for i in data:
        existingRoleId.append(i[2])
    # get all active roles where active = 0
    query = "SELECT * FROM LJRole WHERE status = 1"
    cursor.execute(query)
    ljRoles = cursor.fetchall()
    ljFilteredRoles = []
    existingRoles = []
    
    for role in ljRoles:
        # get roles that are not in existing learning journeys
        if role[0] not in existingRoleId:
            ljFilteredRoles.append(role)
        else:
            existingRoles.append(role)
    return jsonify(
        {
            "data": [ljFilteredRoles, existingRoles]
        }
    ), 200
# [END] Function to GET nested list of Unselected and Selected active roles

# [START] Function to GET relevant skills ID for a specific role ID
def get_skills_id(ljRole_Id):
    query1="SELECT skill_id FROM LJRole_Skill WHERE ljrole_id = " + str(ljRole_Id)
    cursor.execute(query1)
    return cursor.fetchall()
# [END] Function to GET relevant skills ID for a specific role ID

# [START] Function to GET active skill details for a specified list of skills ID
def get_active_skill(skillsId):
    skillsIdQuery = "("
    for item in skillsId:
        skillsIdQuery += str(item[0]) + ","
    skillsIdQuery = skillsIdQuery[:-1]
    skillsIdQuery += ")"
    query = "SELECT * FROM Skill WHERE status = 1 and skill_id in" + str(skillsIdQuery)
    cursor.execute(query)
    return cursor.fetchall()
# [END] Function to GET active skill details for a specified list of skills ID

# [START] Function to GET and Return active skill details for a specified list of skills ID in jsonify
@app.route("/view_active_skills/<int:ljRole_Id>")
def view_active_skills(ljRole_Id):
    # get relevant skills ID matched with roleId
    skillsId = get_skills_id(ljRole_Id)
    
    # get skills that match skills id retrieved earlier and are active 
    skills = get_active_skill(skillsId)
    return jsonify(
        {
            "data": skills
        }
    ), 200
# [END] Function to GET and Return active skill details for a specified list of skills ID in jsonify

# [START] Function to GET newly created learning journey ID
def getLjId():
    query = "SELECT MAX(ljourney_id) FROM LearningJourney"
    cursor.execute(query)
    data = cursor.fetchall()
    id = data[0][0]
    return id
# [END] Function to GET newly created learning journey ID

# [START] Function to CREATE new learning journey 
@app.route("/create_lj", methods=["POST"])
def create_lj():
    # check for missing inputs
    data = request.get_json()
    if not all(key in data.keys() for
               key in ('staffId', 'selectedRole', 'selectedCourses')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
  
    # if form validation succesful
    try:
        staffId = data['staffId']
        selectedRole = data['selectedRole']
        query = "INSERT INTO LearningJourney (staff_id, ljrole_id, completion_status) VALUES (%s, %s, %s);"

        lj_data = (staffId, selectedRole[0], 'Incomplete')
        cursor.execute(query, lj_data)
        db_connection.commit()

        # get new learning journey Id
        newLjId = getLjId()

        selectedCourses = data['selectedCourses']
        for course in selectedCourses:
            query2 = "INSERT INTO LJ_Course VALUES (%s, %s)"
            course_data = (newLjId, course[0])
            cursor.execute(query2, course_data)
            db_connection.commit()

        return jsonify("success"), 201

    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500
# [END] Function to CREATE new learning journey 

# --------- Staff Learning Journey Creation Functions ---------
# --------------------------- End -----------------------------


# ---------- Staff View ALL Learning Journey Functions ----------
# --------------------------- Start ---------------------------

# [START] Function to get role name for a specific role ID
def get_role_name(roleId):
    query = "SELECT ljrole_name FROM LJRole WHERE ljrole_id =" + str(roleId)
    cursor.execute(query)
    ljRoleName = cursor.fetchall()
    ljRoleName = ljRoleName[0][0]
    return ljRoleName
# [END] Function to get role name for a specific role ID

# [START] Function to view ALL learning journey for a specific staff
@app.route("/view_AllLj/<int:staffId>")
def get_all_lj(staffId):
    lj_list = get_all_staff_lj(staffId)
    lj_descriptive_list = []
    for lj in lj_list:
        # get ljid
        ljourney_id = lj[0]
        
        data = []
        # get role name
        roleId = lj[2]
        ljRoleName = get_role_name(roleId)
        
        # get relevant skills ID matched with roleId
        skillsId = get_skills_id(roleId)

        # get skills that match skills id retrieved earlier and are active 
        skills = get_active_skill(skillsId)
        skillNames=""
        for skill in skills:
            if skill != skills[-1]:
                skillNames += (skill[1]) + ", "
            else:
                skillNames += (skill[1])
       
        # get status
        status = lj[3]

        # append as a list to lj_descriptive_list
        data = [ljourney_id, roleId, ljRoleName, skillNames, status]
        lj_descriptive_list.append(data)
    return jsonify(
        {
            "data": lj_descriptive_list
        }
    ), 200
# [END] Function to view ALL learning journey for a specific staff
# ---------- Staff View ALL Learning Journey Functions ---------
# --------------------------- End ---------------------------



# ------- Staff View Learning Journey Details Functions --------
# --------------------------- Start ---------------------------

# [START] Function to get learning journey courses ID in a specific learning journey
def get_lj_courses_id(ljourney_id):
    query = "SELECT course_id FROM LJ_Course WHERE ljourney_id = " + str(ljourney_id)
    cursor.execute(query)
    ljCourseIdList= cursor.fetchall()
    return ljCourseIdList
# [END] Function to get learning journey courses ID in a specific learning journey

# [START] Function to course details based on a specific course ID
def get_course_details(courseId):
    query = "SELECT * from Course WHERE course_status='Active' AND course_id='" + str(courseId) + "'"
    cursor.execute(query)
    return cursor.fetchall()
# [END] Function to course details based on a specific course ID

# [START] Function to get course registration details for a specific staff ID
def get_course_registration_by_staffId(staffId, courseId):
    query = "SELECT course_id, reg_status, completion_status FROM Registration WHERE staff_id=" + str(staffId[0][0]) + " AND course_id='" + str(courseId) + "'"
    cursor.execute(query)
    return cursor.fetchall()
# [END] Function to get course registration details for a specific staff ID


# [START] Function to GET all details (ljourneyId, roleName, skillId, skillName, courseId, courseName, courseDetails) of a specific learning journey ID
@app.route("/view_LjDetails/<int:ljourney_id>")
def view_LjDetails(ljourney_id):
    ljDetails = get_lj_details(ljourney_id)
    
    roleId = ljDetails[0][2]
    roleName= get_role_name(roleId)
    
    skillsId = get_skills_id(roleId)
    skills = get_active_skill(skillsId)
    skillList = []

    # creating skillList where format = [[skillId, skill 1, (acquired/unacquired)], [chosen course names, (completed/ongoing/registered/waitlist/not registered)]]
    for skill in skills:
        skillCourseDetails = []
        courseList = []
        skillId = skill[0]
        
        # get courses under skill ID
        courses_in_skill = get_course_by_skillId(skillId)
        skillAcquired = False
        
        # check if course chosen
        for course in courses_in_skill:
            if course in get_lj_courses_id(ljourney_id):
                courseDetails = (get_course_details(course[0]))
                courseId = courseDetails[0][0]
                courseName = courseDetails[0][1]
                
                # check course status and registration
                # get staffid
                staffId = get_lj_details(ljourney_id)
                staffId = str(staffId[0][1])

                # get course status and registration
                courseStatusDetails = get_course_registration_by_staffId(staffId, courseId)
                
                # extract actual status
                if courseStatusDetails == []:
                    courseStatus = "Register Now"
                else:
                    if courseStatusDetails[0][2] == '':
                        courseStatus = courseStatusDetails[0][1]
                    else:
                        courseStatus = courseStatusDetails[0][2]

                # match skill acquired with status
                if courseStatus == "Completed":
                    skillAcquired = True
                courseList.append([courseId, courseName, courseStatus])
        
        skillCourseDetails = [[skillId, skill[1], skillAcquired], courseList]
        skillList.append(skillCourseDetails)
    
    status = ljDetails[0][3]
    result = [ljourney_id, roleName, skillList, status]
    return jsonify(
        {
            "data": result
        }
    ), 200
# [END] Function to GET all details (ljourneyId, roleName, skillId, skillName, courseId, courseName, courseDetails) of a specific learning journey ID

# [START] Function to DELETE a learning journey based on learning journey ID
@app.route("/deleteLearningJourney/<int:selectedLj>", methods=["DELETE"])
def deleteLearningJourney(selectedLj):
    if (request.method == 'DELETE'):
        # delete from ljcourse table
        query2 = "DELETE FROM LJ_Course WHERE ljourney_id =" + str(selectedLj)
        cursor.execute(query2)
        db_connection.commit()

        # delete from learningjourney table
        query = "DELETE FROM LearningJourney WHERE ljourney_id =" + str(selectedLj)
        cursor.execute(query)
        db_connection.commit()
        
        return jsonify("success", 201)

    else:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500
# [END] Function to DELETE a learning journey based on learning journey ID

# ------- Staff View Learning Journey Details Functions --------
# ---------------------------- End -----------------------------


# -------- Staff Add Learning Journey Courses Functions ---------
# ---------------------------- End -----------------------------
# [START] Function to GET learning journey based on a specific learning journey ID
def get_lj_details(ljourney_id):
    query = "SELECT * FROM LearningJourney WHERE ljourney_id =" + str(ljourney_id)
    cursor.execute(query)
    return cursor.fetchall()
# [END] Function to GET learning journey based on a specific learning journey ID

# [START] Function to GET relevant courses that has not been added to a selected learning journey 
@app.route("/viewCoursesToAdd/<int:ljourney_id>")
def viewCoursesToAdd(ljourney_id):
    ljDetails = get_lj_details(ljourney_id)
    
    roleId = ljDetails[0][2]
    roleName= get_role_name(roleId)
    
    skillsId = get_skills_id(roleId)
    skills = get_active_skill(skillsId)
    skillList = []

    # creating skillList where format = [[skillId, skill 1, (acquired/unacquired)], [chosen course names, (completed/ongoing/registered/waitlist/not registered)]]
    for skill in skills:
        skillCourseDetails = []
        courseList = []
        skillId = skill[0]
        
        # get courses under skill
        courses_in_skill = get_course_by_skillId(skillId)
        skillAcquired = False
        
        # check if course not chosen
        for course in courses_in_skill:
            if course not in get_lj_courses_id(ljourney_id):
                courseDetails = (get_course_details(course[0]))
                
                if courseDetails != []:
                    courseId = courseDetails[0][0]
                    courseName = courseDetails[0][1]
                    courseDesc = courseDetails[0][2]
                    
                    # check course status and registration
                    # get staffid        
                    staffId = get_lj_details(ljourney_id)
                    staffId = str(staffId[0][1])

                    # get course status and registration
                    courseStatusDetails = get_course_registration_by_staffId(staffId, courseId)
                    
                    # extract actual status
                    if courseStatusDetails == []:
                        courseStatus = "Incomplete"
                    else:
                        if courseStatusDetails[0][2] == '':
                            courseStatus = courseStatusDetails[0][1]
                        else:
                            courseStatus = courseStatusDetails[0][2]

                    courseList.append([courseId, courseName, courseStatus, courseDesc])
        
        skillCourseDetails = [[skillId, skill[1]], courseList]
        skillList.append(skillCourseDetails)
    
    status = ljDetails[0][3]
    result = [ljourney_id, roleName, skillList, status]
    return jsonify(
        {
            "data": result
        }
    ), 200
# [END] Function to Get relevant courses that has not been added to a selected learning journey 


# [START] Function to add courses from specific learning journey
@app.route("/addCoursesToLj", methods=["POST"])
def addCoursesToLj():
    # check for missing inputs
    data = request.get_json()
    if not all(key in data.keys() for
               key in ('selectedLj', 'selectedCourses')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
  
    # if form validation succesful
    try:
        selectedLj = data['selectedLj']
        selectedCourses = data['selectedCourses']
        for course in selectedCourses:
            query = "INSERT INTO LJ_Course VALUES (%s, %s)"
            course_data = (selectedLj, course)
            cursor.execute(query, course_data)
            db_connection.commit()
        return jsonify("success"), 201

    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500
# [END] Function to add courses from specific learning journey

# -------- Staff Add Learning Journey Courses Functions ---------
# ---------------------------- End -----------------------------


# ------ Staff Remove Learning Journey Courses Functions -------
# --------------------------- Start -----------------------------

# [START] Function to remove courses from specific learning journey
@app.route("/removeCoursesFromLj", methods=["POST"])
def removeCoursesFromLj():
    # check for missing inputs
    data = request.get_json()
    
    if not all(key in data.keys() for
               key in ('selectedLj', 'selectedCourses')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
  
    # if form validation succesful
    try:
        selectedLj = data['selectedLj']
        selectedCourses = data['selectedCourses']
        for course in selectedCourses:
            query = "DELETE FROM LJ_Course WHERE ljourney_id = (%s) AND course_id= (%s)"
            course_data = (selectedLj, course)
            cursor.execute(query, course_data)
            db_connection.commit()
        return jsonify("success"), 201

    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500
# [END] Function to remove courses from specific learning journey

# ------ Staff Remove Learning Journey Courses Functions -------
# ---------------------------- End ------------------------------

   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
