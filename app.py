from flask import render_template,url_for

from models import db,Post,app


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)