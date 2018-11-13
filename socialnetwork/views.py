from .models import User, find_user
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from .config import Config 
from .forms import LoginForm, RegisterForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


loginManager = LoginManager()
app = Flask(__name__)
app.config.from_object(Config)
loginManager.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = find_user(username=form.username.data)

        if user:
            if check_password_hash(user.password, form.password.data)
            login_user(user, remember=form.remember.data)
            
            # figure out where to redirect to after this
            return redirect(url_for('dashboard'))

        return '<h1> Invalid Username or Password'

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form=form.password.data, method='sha256')
        user = User(
            firstname=form.firstname.data, 
            lastname=form.lastname.data, 
            gender=form.gender.data, 
            dob=form.dob.data, 
            email=form.email.data, 
            username=form.username.data, 
            password=hashed_password
        )
        user.register()
        # Create HTML for postregistration
        return redirect(url_for('postregistration'))


