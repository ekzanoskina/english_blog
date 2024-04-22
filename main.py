from flask import Flask, render_template, flash, request, session, redirect, url_for, send_from_directory, jsonify
from flask_admin import Admin
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_user, logout_user, user_logged_in

from models import *
from forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from views import *
from flask_wtf.csrf import CSRFProtect

# Initialize the Flask application
app = Flask(__name__)
# Setup CSRF protection
csrf = CSRFProtect(app)
# Configuring secret key required for sessions and CSRF protection
app.secret_key = 'sansal54'

# Configure the SQLite database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog_database.db"
# Initialize the SQLAlchemy object with Flask app
db.init_app(app)
# Set CKEditor package type
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
# Configure how many posts will be displayed at most per page
app.config['POSTS_PER_PAGE'] = 5

# Create all tables on application start
with app.app_context():
    db.create_all()

# Setup Flask-Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Setup Flask-Admin and add views for different models
admin = Admin(app, name='My Admin Panel', template_mode='bootstrap4')
admin.add_view(UserAdmin(User, db.session))
admin.add_view(PostAdmin(Post, db.session))
admin.add_view(CategoryAdmin(Category, db.session))

# Initialize CKEditor with our Flask app
ckeditor = CKEditor(app)

# Route for the home page that lists blog posts with pagination
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # Try to get the 'page' argument in the URL, defaulting to 1 if it's not provided
    page = request.args.get('page', 1, type=int)
    # Query and paginate the posts
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=app.config.get('POSTS_PER_PAGE'), error_out=False)
    # Query all categories
    categories = Category.query.all()
    # Render the index page with the posts and categories
    return render_template('index.html', all_posts=posts.items, pagination=posts, categories=categories)

# Route for the registration page
@app.route("/register", methods=["POST", "GET"])
def register():
    # Create instance of registration form
    register_form = RegistrationForm()
    # Process the form on submission
    if register_form.validate_on_submit():
        # Extract form data
        email = register_form.email.data
        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        username = register_form.username.data
        password = register_form.password.data
        confirm_password = register_form.confirm_password.data

        # Check if the email or username exists in the database
        email_exist = User.query.filter_by(email=email).first()
        user_exist = User.query.filter_by(username=username).first()

        # Show appropriate error message or create the user if the provided information is unique
        if email_exist:
            flash('Email is already exist', category='error')
        elif user_exist:
            flash('Username is already taken', category='error')
        elif password != confirm_password:
            flash('Passwords are not matching', category='error')
        else:
            # Password hashing for security
            new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(f"Hi {first_name + ' ' + last_name}, Your account has been successfully created!", 'success')
            return redirect(url_for('index'))
    # Render registration template
    return render_template("register.html", form=register_form)

# Route for login page
@app.route('/login', methods=["GET", "POST"])
def login():
    # Instantiate login form
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # Query user by email
        user = User.query.filter_by(email=login_form.email.data).first()
        # Validate user and password
        if not user:
            flash("That email doesn't exist, please try again.")
        elif not check_password_hash(user.password, login_form.password.data):
            flash("Password incorrect, please try again.")
        else:
            login_user(user)
            return redirect(url_for('index'))
    # Render login template
    return render_template("login.html", form=login_form)

# Route to handle user logout
@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('index'))

# Callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for displaying a single post
@app.route("/<int:post_id>", methods=["GET"])
def show_single_post(post_id):
    # Get the post by ID or return 404 if not found
    post = Post.query.get_or_404(post_id)
    # Query all categories
    all_categories = Category.query.all()
    # Determine which functions to show depending on the user's authentication status
    comment_input_func = 'ShowCommentInput' if current_user.is_authenticated else 'DisplayPopup'
    like_func = 'LetLike' if current_user.is_authenticated else 'DisplayPopup'
    # Render the single post template with the required context variables
    return render_template("single_post.html", post=post, comment_input_func=comment_input_func, like_func=like_func, categories=all_categories)


# Define a route to handle POST requests for submitting comments
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    # Extract comment_text and post_id from the incoming JSON payload
    comment_text = request.json['comment']
    post_id = request.json['post_id']

    # Create a new Comment object with the current user's ID, comment_text, and post_id
    comment = Comment(author=current_user.id, text=comment_text, post_id=post_id)

    # Add the new comment to the database session and commit it to save changes
    db.session.add(comment)
    db.session.commit()

    # Return a JSON response indicating success with additional comment details
    return jsonify({"success": True, "comment": comment_text, "user": current_user.full_name,
                    'date_posted': comment.date_posted_str, 'image_path': current_user.image_file})


# Define a route to handle POST requests for toggling likes on a post
@app.route('/toggle_like', methods=['POST'])
def toggle_like():
    # Retrieve the post_id from the incoming JSON payload, using .get for safer access
    post_id = request.json.get('post_id')

    # Retrieve all likes related to the specified post_id
    likes = Like.query.filter_by(post_id=post_id).all()
    liked = False  # Initialize variable to track whether the current user liked the post

    # Check if the user is authenticated before proceeding
    if current_user.is_authenticated:
        # Check if the current user has already liked the post
        liked = bool(Like.query.filter_by(post_id=post_id, author=current_user.id).all())

        # If the post is already liked, remove the like
        if liked:
            db.session.delete(Like.query.filter_by(post_id=post_id, author=current_user.id).first())
            db.session.commit()
        else:
            # If the post is not liked, add a new like
            like = Like(post_id=post_id, author=current_user.id)
            db.session.add(like)
            db.session.commit()

    # Return a JSON response with the updated likes count and liked status
    return jsonify({'likes_count': len(likes), 'liked': liked})


# Check if the script is the main program and run the app in debug mode if it is
if __name__ == '__main__':
    app.run(debug=True)
