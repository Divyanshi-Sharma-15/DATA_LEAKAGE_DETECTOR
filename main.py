from flask import Flask, render_template, request, redirect, url_for, flash
from Models.db import db
import os
from dotenv import load_dotenv
from Models.model import Users as registerUser
from Generator.leogen import intergers
load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("Sqlite_path")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            return redirect(url_for('main'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

# Define the route for the main application page


@app.route("/create_account", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        Firstaname = request.form['firstname']
        Lastname = request.form['lastname']
        selectLevel = request.form['selectLevel']
        email = request.form['email']
        if Firstaname == '' or Lastname == '' or selectLevel == '' or email == '':
            error = "All field required"
            return render_template('createAccount.html', error=error)
        else:
            data = registerUser(firstname=Firstaname, Lastname=Lastname,
                                role=selectLevel, email=email, userId=intergers.generate())
            db.session.add(data)
            db.session.commit()
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
