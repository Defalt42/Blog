from flask import Flask, request, redirect, url_for, render_template, jsonify, flash, abort
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_required, current_user, UserMixin, logout_user, login_user
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_login.utils import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, SignupForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

db = SQLAlchemy(app)

api = Api(app)

app.config['SECRET_KEY'] = 'aksjdfkjdjfkjdkjfkajd34232322and'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    sub_title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def handle_needs_login():
    return redirect(url_for('login', next=request.endpoint))

# REST API
class Posts(Resource):
    def get(self):
        post = Post.query.order_by(Post.pub_date.desc()).all()
        return jsonify({'Posts': ['Post 1']})

api.add_resource(Posts, '/posts')

# MAIN ROUTES
@app.route("/")
def index():
    posts = Post.query.order_by(Post.pub_date.desc()).all()

    return render_template("index.html", posts=posts)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/<int:id>")
def post(id):
    post = Post.query.get(id)

    return render_template("post.html", post=post)

@app.route('/addpost', methods=['GET','POST'])
@login_required
def add_post():
    if request.form:
        author = current_user.name
        post = Post(author=author, title=request.form['title'], 
            sub_title=request.form['sub_title'], content=request.form['content'])
        
        db.session.add(post)

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            # error, there already is a user using this bank address or other
            # constraint failed

    return render_template('addpost.html')

# AUTH ROUTES

def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)

                return redirect_dest(fallback=url_for('index'))
            else:
                flash('Incorrect email or password! Please try again.')
                return redirect(url_for('login')) 
        else:
            flash('Incorrect email or password! Please try again.')
            return redirect(url_for('login'))
    
    return render_template("login.html", login_form=login_form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            flash('That user already exists.')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        user = User(email=email, name=name, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Account created successfully!')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)