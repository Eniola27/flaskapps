from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField,PasswordField
from wtforms.validators import Email, DataRequired,EqualTo,Length

# class RegForm(FlaskForm):
#     fname = StringField("FirstName",validators=[DataRequired(message="You must input your firstname")])
#     lname = StringField("Last Name",validators=[Length(min=5,message="Your name must not be less than 5 characters")])
#     usermail =StringField("Email",validators=[Email(message="invalid email format"),DataRequired(message="Email must be supplied"),Length(min=5,message="email is too short")])
#     pwd =PasswordField("Enter Password",validators=[DataRequired(message='password is required')])
#     confpwd=PasswordField("Confirm Password",validators=[EqualTo('pwd',message="both password must match")])
#     profile = TextAreaField("Your Profile")
#     btnsubmit = SubmitField("Register!")


# class LogForm(FlaskForm):
#    username=StringField("username",validator=[DataRequired(message="You must enter your username")])
#    pwd =PasswordField("Enter Password",validators=[DataRequired(message='password is required')]) 






    