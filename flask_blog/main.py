from flask import Blueprint, render_template, url_for, request, redirect

from . import db
from .models import Post, Category
from sqlalchemy.exc import IntegrityError


main = Blueprint('main', __name__)

@main.route("/")
def index():
    posts = Post.query.order_by(Post.pub_date.desc()).all()

    return render_template("index.html", posts=posts)


@main.route('/new-post', methods=['GET','POST'])
def add_post():
    if request.form:
        category_name = request.form['category']
        category = Category.query.filter_by(name=category_name).first()
        post = Post(author=request.form['author'], title=request.form['title'], 
            category=category,
            content=request.form['content'])
        
        db.session.add(post)

        try:
            db.session.commit()
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            # error, there already is a user using this bank address or other
            # constraint failed

    categories = Category.query.all()

    return render_template('newpost.html', categories=categories)

@main.route('/new-category', methods=['GET', 'POST'])
def add_category():
    if request.form:
        category = Category(name=request.form['category'])
        db.session.add(category)
        try:
            db.session.commit()
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            # error, there already is a user using this bank address or other
            # constraint failed

        
    return render_template('newcategory.html')