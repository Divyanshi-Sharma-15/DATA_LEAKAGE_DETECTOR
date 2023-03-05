import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from Models.db import db
import os
from dotenv import load_dotenv
from Models.model import Users as registerUser
from Generator.leogen import intergers
import logging
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
                logger.info('User {} Logg in Attempt Failed'.format(email))
                return render_template('login.html', error=error)
            if databaseResponse.password != password:
                error = 'Wrong username or password.Try again'
                logger.info('User {} Logg in Attempt Failed'.format(email))
                return render_template('login.html', error=error)
            else:
                flash('You have been logged in successfully!', 'success')
                logger.info('User {} logged in successfully'.format(email))
                return redirect(url_for('main'))
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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True)
