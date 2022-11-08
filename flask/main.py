from flask import Flask, request, jsonify, request, redirect
import os
from flask_cors import CORS
import mysql.connector as mysql
from skillManagementFunctions.skillManagementFunctions import skillManagementFunctions
from roleManagementFunctions.roleManagementFunctions import roleManagementFunctions
from courseManagementFunctions.courseManagementFunctions import courseManagementFunctions
from ljManagementFunctions.ljManagementFunctions import ljManagementFunctions
from mappingFunctions.mappingFunctions import mappingFunctions




app = Flask(__name__, template_folder='../htdocs')
app.register_blueprint(skillManagementFunctions)
app.register_blueprint(roleManagementFunctions)
app.register_blueprint(courseManagementFunctions)
app.register_blueprint(ljManagementFunctions)
app.register_blueprint(mappingFunctions)


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
                return redirect("http://localhost:8888/SPMProject/SPM%2520Project/htdocs/statusOfImportSuc.html")
            except mysql.errors.IntegrityError:
                return redirect("http://localhost:8888/SPMProject/SPM%2520Project/htdocs/statusOfImportDup.html")
            except Exception:
                return redirect("http://localhost:8888/SPMProject/SPM%2520Project/htdocs/statusOfImportUnCom.html")
        else:
                return redirect("http://localhost:8888/SPMProject/SPM%2520Project/htdocs/statusOfImportOnl.html")
    else:
        return redirect("http://localhost:8888/SPMProject/SPM%2520Project/htdocs/coursesManagement.html")

# [END] Function to IMPORT all courses from CSV file

if __name__ == '__main__':
    # from waitress import serve
    app.run(host='0.0.0.0', port=5000, debug=True)
    # serve(app, host='0.0.0.0', port=5000)