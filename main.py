from flask import Flask, render_template, flash, request, session, redirect, url_for, send_from_directory, jsonify
from flask_admin import Admin
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_user, logout_user, user_logged_in

from models import *
from forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from views import *


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog_database.db"
app.secret_key = 'sansal54'
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
# initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

admin = Admin(app, name='My Admin Panel', template_mode='bootstrap4')

admin.add_view(UserAdmin(User, db.session))
admin.add_view(PostAdmin(Post, db.session))

ckeditor = CKEditor(app)

@app.route('/')
def index():
    post = Post(title='first', content='Разрешите фоновую активность. Еще одно возможное решение вашей проблемы - отключить ограничения фонового выполнения. Сделайте необходимые')
    db.session.add(post)
    db.session.commit()
    return render_template('index.html')

@app.route('/posts')
def get_all_posts():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', all_posts=posts)



@app.route("/register", methods=["POST", "GET"])
def register():
    # If the request method is POST
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        if form.image.data:
            image_data = request.FILES[form.image.name].read()
            open(os.path.join('static', form.image.data), 'w').write(image_data)
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
    return render_template("register.html", form=form)

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


@app.route("/<int:post_id>", methods=["GET"])
def show_single_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.is_authenticated:
        comment_input_func = 'ShowCommentInput'
        like_func = 'LetLike'
    else:
        comment_input_func = 'DisplayPopup'
        like_func = 'DisplayPopup'
    return render_template("single_post.html", post=post, comment_input_func=comment_input_func, like_func=like_func)


@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    comment_text = request.json['comment']
    post_id = request.json['post_id']
    comment = Comment(author=current_user.id, text=comment_text, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"success": True, "comment": comment_text, "user": current_user.full_name, 'date_posted': str(comment.date_posted), 'image_path': current_user.image_file})

@app.route('/toggle_like', methods=['POST'])
def toggle_like():
    post_id = request.json.get('post_id')
    likes = Like.query.filter_by(post_id=post_id).all()
    liked = False
    if current_user.is_authenticated:
        liked = bool(Like.query.filter_by(post_id=post_id, author=current_user.id).all())
        if liked:
            db.session.delete(Like.query.filter_by(post_id=post_id, author=current_user.id).first())
            db.session.commit()
        else:
            like = Like(post_id=post_id, author=current_user.id)
            db.session.add(like)
            db.session.commit()
    return jsonify({'likes_count': len(likes), 'liked': liked})

if __name__ == '__main__':
    app.run(debug=True)
