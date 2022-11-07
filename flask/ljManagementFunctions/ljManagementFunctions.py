from flask import Flask, request, jsonify, request, Blueprint
from flask_cors import CORS
import mysql.connector as mysql

ljManagementFunctions = Blueprint('ljManagementFunctions', __name__)

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

CORS(ljManagementFunctions)

# --------- Staff Learning Journey Creation Functions ---------
# --------------------------- Start ---------------------------
# [START] Function to GET all skills based on specified Learning Journey role ID
@ljManagementFunctions.route("/view_skills/<int:ljRole_Id>")
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

# [START] Function to GET active courses based on specified course ID
def getCourseByID(course_id):
    query = "SELECT DISTINCT * FROM Course WHERE course_status='Active'" + "AND course_id ='" + str(course_id)+"'"
    cursor.execute(query)
    # print(cursor.fetchall())
    return cursor.fetchall()
# [END] Function to GET active courses based on specified course ID

# [START] Function to GET courses ID bsed on a specific skill ID
def get_course_by_skillId(skillId):
        query = "SELECT course_id FROM Course_Skill WHERE skill_id=" + str(skillId)
        cursor.execute(query)
        return cursor.fetchall()    
# [END] Function to GET courses ID based on a specific skill ID

# [START] Function to GET skill description and courses based on a specified skill ID
@ljManagementFunctions.route("/view-course-skills/<int:skillID>")
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

# [START] Function to get staff learning journey
def get_all_staff_lj(staffId):
    query = "SELECT * FROM LearningJourney WHERE staff_id=" + str(staffId)
    cursor.execute(query)
    return cursor.fetchall()
# [END] Function to get staff learning journey

# [START] Function to GET nested list of Unselected and Selected active roles
@ljManagementFunctions.route("/view_filteredLjRoles/<int:staffId>")
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
@ljManagementFunctions.route("/view_active_skills/<int:ljRole_Id>")
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
@ljManagementFunctions.route("/create_lj", methods=["POST"])
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
@ljManagementFunctions.route("/view_AllLj/<int:staffId>")
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
    query = "SELECT course_id, reg_status, completion_status FROM Registration WHERE staff_id=" + str(staffId) + " AND course_id='" + str(courseId) + "'"
    cursor.execute(query)
    return cursor.fetchall()
# [END] Function to get course registration details for a specific staff ID

# [START] Function to GET courses ID bsed on a specific skill ID
def get_course_by_skillId(skillId):
        query = "SELECT course_id FROM Course_Skill WHERE skill_id=" + str(skillId)
        cursor.execute(query)
        return cursor.fetchall()    
# [END] Function to GET courses ID based on a specific skill ID

# [START] Function to GET all details (ljourneyId, roleName, skillId, skillName, courseId, courseName, courseDetails) of a specific learning journey ID
@ljManagementFunctions.route("/view_LjDetails/<int:ljourney_id>")
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
@ljManagementFunctions.route("/deleteLearningJourney/<int:selectedLj>", methods=["DELETE"])
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
@ljManagementFunctions.route("/viewCoursesToAdd/<int:ljourney_id>")
def viewCoursesToAdd(ljourney_id):
    ljDetails = get_lj_details(ljourney_id)
    
    roleId = ljDetails[0][2]
    roleName= get_role_name(roleId)
    
    skillsId = get_skills_id(roleId)
    skills = get_active_skill(skillsId)
    print(skills)
    skillList = []

    # creating skillList where format = [[skillId, skill 1, (acquired/unacquired)], [chosen course names, (completed/ongoing/registered/waitlist/not registered)]]
    for skill in skills:
        skillCourseDetails = []
        courseList = []
        skillId = skill[0]
        
        # get courses under skill
        courses_in_skill = get_course_by_skillId(skillId)
        
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
                        print(courseStatusDetails)
                        courseStatus = "Incomplete"
                    else:
                        print(courseStatusDetails[0][2])
                        if courseStatusDetails[0][2] == '':
                            courseStatus = courseStatusDetails[0][1]
                        else:
                            courseStatus = courseStatusDetails[0][2]

                    courseList.append([courseId, courseName, courseStatus, courseDesc])
        
        skillCourseDetails = [[skillId, skill[1]], courseList]
        skillList.append(skillCourseDetails)
        print(skillCourseDetails)
    status = ljDetails[0][3]
    result = [ljourney_id, roleName, skillList, status]
    return jsonify(
        {
            "data": result
        }
    ), 200
# [END] Function to Get relevant courses that has not been added to a selected learning journey 


# [START] Function to add courses from specific learning journey
@ljManagementFunctions.route("/addCoursesToLj", methods=["POST"])
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
@ljManagementFunctions.route("/removeCoursesFromLj", methods=["POST"])
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