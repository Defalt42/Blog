from flask import Blueprint, render_template, url_for, request, redirect

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm, SignupForm
from sqlalchemy.exc import IntegrityError
from flask_login import login_user

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        user = User()
        login_user(user)

    return render_template("login.html", login_form=login_form)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('logout.html')