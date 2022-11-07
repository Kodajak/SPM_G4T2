from flask import Flask, request, jsonify, request
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

   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
