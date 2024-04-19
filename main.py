from flask import Flask, render_template, flash, request, session, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, user_logged_in

from models import *
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog_database.db"
app.config.update(SECRET_KEY=os.urandom(24))
# initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def get_all_posts():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', all_posts=posts)



@app.route("/register", methods=["POST", "GET"])
def register():
    # If the request method is POST
    if request.method == "POST":
        # Get the form data
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check if the email or username already exists in the database
        email_exist = User.query.filter_by(email=email).first()
        user_exist = User.query.filter_by(username=username).first()

        # Validate the form data
        if email_exist:
            flash('Email is already exist', category='error')
        elif user_exist:
            flash('Username is already taken', category='error')
        elif password != confirm_password:
            flash('Passwords are not matching', category='error')
        elif len(username) < 3:
            flash('Username is too short', category='error')
        elif len(password) < 6:
            flash('Password is too short', category='error')
        elif len(email) < 4:
            flash("Email is invalid", category='error')
        # If the form data is valid
        else:
            # Create a new user object
            new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=generate_password_hash(password) )
            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()
            # Log the user in
            login_user(new_user, remember=True)
            print(user_logged_in)
            flash(f"Hi {first_name + ' ' + last_name}, Your account has been successfully created!",'success')
            # Redirect the user to the home page
            return redirect(url_for('index'))
    # If the request method is GET
    # render the signup template
    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if not user:
            flash("That email doesn't exist, please try again.")
        elif not check_password_hash(user.password, login_form.password.data):
            flash("Password incorrect, please try again.")
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user):
    return User.query.get(int(user))

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments =Comment.query.order_by(Comment.id.desc()).all()
    image_file = url_for('static', filename='profile_pics/' + post.author.image_file)
    post.views += 1
    db.session.commit()
    return render_template('post.html', title=post.title, comments=comments, post=post, image_file=image_file)




# redirect example
# @app.route('/home')
# def home():
#     # do some logic, example get post id
#     if my_post_id:
#        # **Note:** post_id is the variable name in the open_post route
#        # We need to pass it as **post_id=my_post_id**
#        return redirect(url_for(app.open_post,post_id=my_post_id))
#     else:
#        print("Post you are looking for does not exist")
#     return render_template('index.html',title="Home Page")
#
#
# @app.route('/post/<string:post_id>')
# def open_post():
#     return render_template('readPost.html',title="Read Post")

# @app.route('/')
# def show_all():
#     # We are getting all the comments ordered in
#     # descending order of pub_date and passing to the
#     # template via 'comments' variable
#     return render_template('show_all.html',
#         comments=Comments.query.order_by(Comments.pub_date.desc()).all()
#     )
#
# # This view method responds to the URL /new for the methods GET and POST
# @app.route('/new', methods=['GET', 'POST'])
# def new():
#     if request.method == 'POST':
#         # The request is POST with some data, get POST data and validate it.
#         # The form data is available in request.form dictionary.
#         # Check if all the fields are entered. If not, raise an error
#         if not request.form['name'] or not request.form['email'] or not request.form['comment']:
#             flash('Please enter all the fields', 'error')
#         # Check if the email address is valid. If not, raise an error
#         elif not is_email_address_valid(request.form['email']):
#             flash('Please enter a valid email address', 'error')
#         else:
#             # The data is valid. So create a new 'Comments' object
#             # to save to the database
#             comment = Comments(request.form['name'],
#                                request.form['email'],
#                                request.form['comment'])
#             # Add it to the SQLAlchemy session and commit it to
#             # save it to the database
#             db.session.add(comment)
#             db.session.commit()
#             # Flash a success message
#             flash('Comment was successfully submitted')
#             # Redirect to the view showing all the comments
#             return redirect(url_for('show_all'))
#     # Render the form template if the request is a GET request or
#     # the form validation failed
#     return render_template('new.html')


if __name__ == '__main__':
    app.run(debug=True)
