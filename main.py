import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from Models.db import db
import os
from dotenv import load_dotenv
from Models.model import Users as registerUser, Uploaded
from Generator.leogen import intergers
import logging
from werkzeug.utils import secure_filename

from leoWaterMaking import WaterMark

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('audit_trail.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


app = Flask(__name__)
app.secret_key = 'secret_key'


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("Sqlite_path")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/")
def landing_page():
    return render_template("main.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if request.form['email'] == '' and request.form['password'] == '':
            error = "All field required"
            return render_template('login.html')
        else:
            databaseResponse = registerUser.query.filter_by(
                email=email).first()
            if bool(databaseResponse) == False:
                error = 'Wrong username or password.Try again'
                logger.warning('User {} Log in Attempt Failed'.format(email))
                return render_template('login.html', error=error)
            if databaseResponse.password != password:
                error = 'Wrong username or password.Try again'
                logger.warning('User {} Log in Attempt Failed'.format(email))
                return render_template('login.html', error=error)
            else:
                flash('You have been logged in successfully!', 'success')
                session['username'] = email
                logger.info('User {} logged in successfully'.format(email))
                return redirect(url_for('user_profile'))
    else:
        return render_template('login.html')

# Define the route for the main application page


@app.route("/create_account", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        Firstaname = request.form['firstname']
        Lastname = request.form['lastname']
        selectLevel = request.form['selectLevel']
        password = request.form['password']
        email = request.form['email']
        if Firstaname == '' or Lastname == '' or selectLevel == '' or email == '' or password == '':
            error = "All field required"
            return render_template('createAccount.html', error=error)
        else:
            data = registerUser(firstname=Firstaname, Lastname=Lastname,
                                role=selectLevel, email=email, userId=intergers.generate(length=6), password=password)
            db.session.add(data)
            db.session.commit()
            session['username'] = email
            logger.info('User {} registered successfully'.format(email))

            success = "registered successfully"

            return redirect(url_for('main'))
    else:
        return render_template("createAccount.html")


@app.route('/main')
def main():
    # TODO: Display the main application page with the data and functionality required

    return render_template('main.html')


@app.route("/admin/home")
def admin_home():
    databaseResponse = registerUser.query.all()
    NumOfUsers = len(databaseResponse)
    Unproved = 0
    userList = []
    for user in databaseResponse:
        # collectin all users
        userDict = {}
        name = user.firstName+" "+user.Lastname
        userDict["email"] = user.email
        userDict["name"] = name
        userDict["id"] = user.UserId
        userDict['role'] = user.UserRole
        userDict["verified"] = user.Verified
        userList.append(userDict)
        if user.Verified == "False":
            Unproved += 1
        print(user.email)

    return render_template("admin_home.html", numOfUsers=NumOfUsers, UnapprovedUsers=Unproved, Users=userList)


@app.route("/admin/statistics")
def statics():
    databaseResponse = registerUser.query.all()
    for user in databaseResponse:
        print(user.email)


@app.route("/admin/logs")
def all_logs():
    logs = []
    with open("audit_trail.log", 'r') as f:
        lines = f.readlines()
        for line in lines:
            logs.append(line)
    return render_template("Logs.html", logs=logs)


@app.route("/admin/upload/data", methods=['POST', 'GET'])
def update_data():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        doc_name = request.form["document_name"]
        filenameImage = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(
            os.environ.get("server_path"), filenameImage))
        data = Uploaded(title=doc_name, filename=uploaded_file.filename)
        db.session.add(data)
        db.session.commit()

    return render_template("manageData.html")


@app.route("/user/profile")
def user_profile():
    if "username" in session:
        email = session['username']
        user = registerUser.query.filter_by(email=email).first()
        name = user.firstName+" "+user.Lastname
        logger.info('User {} Access profile successfully'.format(email))
        return render_template("userProfile.html", user_email=email, user_name=name)
    else:
        return redirect(url_for(main))


@app.route("/user/access/documents/")
def access_documents():
    documents = Uploaded.query.all()
    documentList = []
    for document in documents:
        documentDict = {}
        documentDict['DocName'] = document.title
        documentDict['fileName'] = document.filename
        documentList.append(documentDict)

    return render_template("Access_documnets.html", documents=documentList)


@app.route("/download/<filename>")
def download(filename):
    if "username" in session:
        email = session['username']
        user = registerUser.query.filter_by(email=email).first()
        name = user.firstName+" "+user.Lastname
        userId = user.UserId
        WaterMark.add_watermark(input_file=filename,
                                output_file=name+"_"+filename, text=userId)
        logger.info('User {} Accessed {}'.format(email, filename))

    return send_file("./Downloaded/"+name+"_"+filename, as_attachment=True)


@app.route("/getStarted")
def helpDirection():
    return render_template("help.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True, host="0.0.0.0")
