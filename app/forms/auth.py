from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
	remember = BooleanField("Remember me")
	submit = SubmitField("Login")

class RegisterForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
	first_name = StringField("First name")
	last_name = StringField("Last name")
	consent = BooleanField("I agree to data storage", validators=[DataRequired()])
	submit = SubmitField("Register")
