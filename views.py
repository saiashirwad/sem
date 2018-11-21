from user import User
from post import Post 
from comment import Comment 

from flask import Flask, render_template, redirect, url_for, session
from flask_session import Session

from config import Config 
from forms import LoginForm, RegisterForm, PostForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap

from datetime import datetime

app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'very secret key'
Session(app)
Bootstrap(app)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():

        user = User.get_user(username=form.username.data)

        if user:

            if check_password_hash(user.password, form.password.data):

                session['user'] = user 

            return redirect(url_for('dashboard'))

        return '<h1> Invalid Username or Password'

    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            firstname=form.firstname.data, 
            lastname=form.lastname.data, 
            gender=form.gender.data, 
            email=form.email.data, 
            username=form.username.data, 
            password=hashed_password
        )

        user.register()

        return redirect(url_for('login'))

    return render_template('registration.html', form=form)



@app.route('/create_post', methods=['GET', 'POST'])
def create_post():

    form = PostForm()
    
    if form.validate_on_submit():  

        if session['user']:

            user_id = session['user'].id 
            text = form.text.data
            title = form.title.data 
            tags = form.tags.data.split()

            post = Post(
                text = text,
                user_id = user_id,
                title = title,
                tags = tags
            )

            post.create()

            return redirect(url_for('dashboard'))

        else:

            return redirect(url_for('login'))

    return render_template('create_post.html', form=form)



@app.route('/dashboard')
def dashboard():

    print(session['user'])

    posts = User.get_posts_by_user(session['user'].username)
    parsed_posts = []

    for post in posts:

        postvar = post['p']

        parsed_posts.append({
        'text': postvar['text'], 
        'date': datetime.fromtimestamp(postvar['created']),
        'tags': postvar['tags'],
        'title': postvar['title'],
        'id': postvar['id']
        })
    
    print(parsed_posts)
    # print(User.get_posts_by_user(session['user'].username)[0]['p']['text'])

    return render_template('dashboard.html', posts=parsed_posts)



@app.route('/logout') 
def logout():

    if session['user']:

        session['user'] = None

    return redirect(url_for('login'))



# @app.route('/profile/<id>')
# def profile(username):

#     pass
#     # return render_template('profile.html', user=session['user'], friends=session['user'].get_friends())



@app.route('/post/<id>', methods=['GET', 'POST'])
def show_post(id):    

    form = CommentForm()

    post = Post.find_by_id(id)
    user_id = session['user'].id 

    if form.validate_on_submit():

        comment = Comment(
            user_id = user_id,
            post_id = id,
            text = form.comment.data
        )

        comment.create()

        return redirect(url_for('show_post', id=id))

    comments = Post.get_post_comments(id)

    print(comments)

    return render_template('post.html', user=session['user'], post=post, form=form, comments=comments)



@app.route('/delete/post/<id>', methods=['GET', 'POST'])
def delete_post(id):

    post = Post.find_by_id(id)

    # Finish deleting logic



@app.route('/profile/<username>')
def profile(username):
    user = User.find_user(username=username)
    if user:
        cur_user = User.find_user(username=current_user.username)
        if cur_user.friends_with(username):
            return render_template('friend.html', user=user)    
        return render_template('notfriend.html', user=user)



@app.route('/friendrequest/<username>')
def send_friend_request(username):
    user = User.find_user(username=username)
    cur_user = User.find_user(username=current_user.username)
    cur_user.request_friendship(username)

    return render_template('notfriend.html', user)

    

app.run('127.0.0.1', '5000')
