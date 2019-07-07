from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # prevent already authenticated user from accessing the /login route
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Use the form-submitted username to lookup the User in the DB.
        # The first() method is used because there is only going to be one or zero results.
        # first() will return the user object if it exists, or None if it does not.
        user = User.query.filter_by(username=form.username.data).first()
        # This will take the password hash stored with the user and determine if the 
        # password entered in the form matches the hash or not.
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # call the flask-login function
        login_user(user, remember=form.remember_me.data)
        # This part will examine the url query string for a 'next' attribute
        # request.args attribute exposes the contents of the query string in a friendly dictionary format
        next_page = request.args.get('next')
        # This is to make the application more secure. An attacker could insert a URL
        # to a malicious site in the `next` argument, so the application only redirects when
        # the URL is relative, which ensures that the redirect stays within the same site as the application.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


from app import db
from app.forms import RegistrationForm


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
