from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')



class RegisterForm(FlaskForm):
    firstname = StringField('first name', validators=[InputRequired()])
    lastname = StringField('last name', validators=[InputRequired()])
    gender = SelectField('gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email(message="Invalid Email!")])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('submit')



class PostForm(FlaskForm):
    title = StringField('Enter your post title:', validators=[InputRequired(), Length(min=5, max=40)])
    text = StringField('Enter your post:', validators=[InputRequired()])
    tags = StringField('Enter tags separated by spaces:', validators=[InputRequired()])
    submit = SubmitField('submit')



# class UserDetailsForm(FlaskForm):
#     bio = StringField('bio', validators=[Length(max=500)])
#     firstName = StringField('first name', default=self.user.firstName)
#     lastName = StringField('last name', default=self.user.lastName)
#     email = StringField('email', default=self.user.email, validators=[Email(message='Invalid Email')])
#     def __init__(self, user):
#         self.user = user 



class CommentForm(FlaskForm):
    comment = StringField('What do you think about this?', validators=[InputRequired()])
    submit = SubmitField('Submit!')



class ChangePasswordForm(FlaskForm):
    previousPassword = PasswordField('Previous Password', validators=[InputRequired(), Length(min=8, max=20)])
    newPassword = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=20)])

