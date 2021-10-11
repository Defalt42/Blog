from flask import render_template, url_for, request, redirect

from models import db, Post, Category, app
from sqlalchemy.exc import IntegrityError

@app.route("/")
def index():
    posts = Post.query.order_by(Post.pub_date.desc()).all()

    return render_template("index.html", posts=posts)


@app.route('/new-post', methods=['GET','POST'])
def add_post():
    if request.form:
        category_name = request.form['category']
        category = Category.query.filter_by(name=category_name).first()
        post = Post(author=request.form['author'], title=request.form['title'], 
            category=category,
            content=request.form['content'])
        
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))

    categories = Category.query.all()

    return render_template('newpost.html', categories=categories)

@app.route('/new-category', methods=['GET', 'POST'])
def add_category():
    if request.form:
        category = Category(name=request.form['category'])
        db.session.add(category)
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            # error, there already is a user using this bank address or other
            # constraint failed

        
    return render_template('newcategory')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)