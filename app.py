from flask import render_template, url_for, request, redirect

from models import db, Post, Category, app


@app.route("/")
def index():
    category_py = Category(name='Python')
    category_photography = Category(name='Photography')

    post_1 = Post(author='Bryan Gilbert', title='Python 101', 
        content='The first step is to start coding.', 
        category=category_py)
    post_2 = Post(author='John Wick', title='Photography Basics', 
        content='Let\'s start with ISO, aperture, and shutter speed.', 
        category=category_photography)

    category_py.posts.append(post_1)
    category_photography.posts.append(post_2)

    db.session.add(category_py)
    db.session.add(category_photography)
    db.session.commit()

    posts = Post.query.all()

    return render_template("index.html", posts=posts)


@app.route('/new-post', methods=['GET','POST'])
def add_post():
    if request.form:
        post = Post(author=request.form['author'], title=request.form['title'], 
            category=request.form['category'],
            content=request.form['content'])
        
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('newpost.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)