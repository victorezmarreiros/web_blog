from flask import Flask, render_template, request, session

from common.database import Database
from models.blog import Blog
from models.user import User

app = Flask(__name__)
app.secret_key = "victor"


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')  # 127.0.0.1:4925/login
def login_template():
    return render_template('login.html')


@app.route('/register')  # 127.0.0.1:4925/register
def register_template():
    return render_template('register.html')


@app.before_first_request
def connect_database():
    Database.connect()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None

    return render_template("profile.html", email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template('profile.html', email=session['email'])


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()
    print(blogs)
    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_title=blog.title)


if __name__ == '__main__':
    app.run(port=4925)
