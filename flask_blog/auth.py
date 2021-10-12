from flask import Blueprint, render_template, url_for, request, redirect

from . import db
from models import Post, Category
from sqlalchemy.exc import IntegrityError


auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('logout.html')