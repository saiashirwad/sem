from .models import User
from flask import Flask, render_template, redirect, url_for, session
from flask_login import LoginManager
from .config import Config 
from .forms import LoginForm, RegisterForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap

'''
Can use session to store current user and all other kinds of shit.
'''

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
        user = User.find_user(username=form.username.data)
        if user:
            if check_password_hash(user.password, form.password.data):
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

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.find_user(username=username)
    if user:
        cur_user = User.find_user(username=current_user.username)
        if cur_user.friends_with(username):
            return render_template('friend.html')    
        return render_template('notfriend.html')


