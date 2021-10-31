from flask import Blueprint, render_template, url_for, request, redirect

from . import db
from .models import Post
from sqlalchemy.exc import IntegrityError
import datetime

main = Blueprint('main', __name__)

@main.route("/")
def index():
    posts = Post.query.order_by(Post.pub_date.desc()).all()

    return render_template("index.html", posts=posts)

@main.route("/contact")
def contact():
    return render_template("contact.html")

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/post/<int:id>")
def post(id):
    post = Post.query.get(id)

    return render_template("post.html", post=post)

@main.route('/addpost', methods=['GET','POST'])
def add_post():
    if request.form:
        post = Post(author=request.form['author'], title=request.form['title'], 
            sub_title=request.form['sub_title'], content=request.form['content'])
        
        db.session.add(post)

        try:
            db.session.commit()
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            # error, there already is a user using this bank address or other
            # constraint failed

    return render_template('addpost.html')