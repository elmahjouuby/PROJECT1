from flask import Flask, render_template, redirect, url_for
from flask.helpers import url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.core import IntegerField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'marouaneelmahjouby'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/Users/Marouane/Desktop/PROJECT1/database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    email = db.Column(db.String(50),unique=True)
    address = db.Column(db.String(50))
    phone = db.Column(db.Numeric(50))
    password = db.Column(db.String(100))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    email = StringField('EMAIL', validators=[InputRequired()])
    password = PasswordField('PASSWORD', validators=[InputRequired()])

class RegisterFrom(FlaskForm):
    email = StringField('EMAIL', validators=[InputRequired(), Email(message="Invalid email"), Length(max=40)])
    firstname = StringField('FIRST NAME', validators=[InputRequired(), Length(min=4,max=30)])
    lastname = StringField('LAST NAME', validators=[InputRequired(), Length(min=4,max=30)])
    address = StringField('ADDRESS', validators=[InputRequired(),Length(max=100)])
    phone = IntegerField('PHONE NUMBER',validators=[InputRequired()])
    password = PasswordField('PASSWORD', validators=[InputRequired(), Length(min=10,max=30)])


@app.route('/home')
@login_required
def home():
    return render_template('home.html', name=current_user.firstname)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect(url_for('home'))
        return "<h1>Invalid Username or Password</h1>"
    return render_template('login.html',form=form)

@app.route('/signup',methods=['GET','POST'])
def signup():
    form = RegisterFrom()
    if form.validate_on_submit():
        #Hashing the password
        hashed_password = generate_password_hash(form.password.data)
        #PUTTING DATA CREATED BY USER INTO THE DATABASE
        new_user = User(email=form.email.data, firstname=form.firstname.data,
        lastname=form.lastname.data, address=form.address.data, phone=form.phone.data, 
        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New user has been created successfully </h1>'
        
    return render_template('sign_up.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)