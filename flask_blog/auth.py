from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login.utils import login_required

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm, SignupForm
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Logged in successfully!')
                return redirect(url_for('main.index'))
            else:
                flash('Incorrect email or password! Please try again.')
                return redirect(url_for('auth.login')) 
        else:
            flash('Incorrect email or password! Please try again.')
            return redirect(url_for('auth.login'))

    return render_template("login.html", login_form=login_form)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            flash('That user already exists.')
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        user = User(email=email, name=name, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Account created successfully!')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('main.index'))