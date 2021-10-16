from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.core import IntegerField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'marouaneelmahjouby'
app.config['SQLALCHEMY_DATABE_URI'] = 'C:/Users/Marouane/Desktop/PROJECT1/users.db'
db = SQLAlchemy(app)



class LoginForm(FlaskForm):
    firstname = StringField('FIRST NAME', validators=[InputRequired(), Length(min=4,max=30)])
    password = PasswordField('PASSWORD', validators=[InputRequired(), Length(min=10,max=30)])

class RegisterFrom(FlaskForm):
    email = StringField('EMAIL', validators=[InputRequired(), Email(message="Invalid email"), Length(max=40)])
    firstname = StringField('FIRST NAME', validators=[InputRequired(), Length(min=4,max=30)])
    lastname = StringField('LAST NAME', validators=[InputRequired(), Length(min=4,max=30)])
    address = StringField('ADRESS', validators=[InputRequired(),Length(max=100)])
    phone = IntegerField('PHONE NUMBER',validators=[InputRequired()])
    password = PasswordField('PASSWORD', validators=[InputRequired(), Length(min=10,max=30)])


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return form.firstname.data 
    return render_template('login.html',form=form)

@app.route('/signup',methods=['GET','POST'])
def signup():
    form = RegisterFrom()
    if form.validate_on_submit():
        return form.email.data
    return render_template('sign_up.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)