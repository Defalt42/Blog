from flask import render_template, url_for, request, redirect

from models import db, Post, Category, app


@app.route("/")
def index():
    posts = Post.query.all()

    return render_template("index.html", posts=posts)


@app.route('/new-post', methods=['GET','POST'])
def add_post():
    if request.form:
        category = Category(name=request.form['category'])
        post = Post(author=request.form['author'], title=request.form['title'], 
            category=category,
            content=request.form['content'])
        
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('newpost.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)