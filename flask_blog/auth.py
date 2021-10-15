from flask import Blueprint, render_template, url_for, request, redirect

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm, SignupForm
from sqlalchemy.exc import IntegrityError


auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    login_form = LoginForm()

    return render_template("login.html", login_form=login_form)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('logout.html')