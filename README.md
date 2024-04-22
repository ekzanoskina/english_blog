# Flask Blog Project

This is a simple blog application built using Flask, a popular Python web framework. The project includes features such as user authentication, CSRF protection, and a SQLite database for storing blog posts.
It also includes an administration feature that allows administrators to create and delete blog posts.

## Screenshots

Home Page:

![Home page](screenshots/index.png?raw=true "Posts")

Single Post Page:
![Single post](screenshots/single_post.png?raw=true "Single post")

Login and Register Pages:

![Login](screenshots/login.png?raw=true "Login")
![Register](screenshots/register.png?raw=true "Register")

Admin Panel and Post Creation Views:

![Admin panel](screenshots/admin_panel.png?raw=true "Admin Panel")
![Admin panel post creation](screenshots/admin_panel_post_creation.png?raw=true "Admin Panel post creation")

Comment and Like Features:

![Comments and likes](screenshots/comment_and_like_features.png?raw=true "Comments and likes")


## Features

- User login and logout
- CSRF protection
- SQLite database for storing blog posts
- Admin Panel and CKEditor for creating and editing blog posts
- Pagination for displaying posts 
- Dynamic comments and likes using Flask and AJAX
- Logged-in-users-only content

## Languages

- Python
- HTML | Jinja
- CSS
- JavaScript

## Technologies

### Backend

- SQLite3
- Flask
- Flask_WTF
- Requests

### Frontend

- JavaScript
- Boostrap

## File Structure

- `main.py`: The main Python file that configures and runs the Flask application.
- `forms.py`: Contains the WTForms classes used for user registration and login.
- `templates/`: Directory containing the HTML templates used for rendering different views.
- `static/`: Directory containing static files such as CSS stylesheets and images.
- `views.py`: Contains views for the admin panel.
- `views.py`: Provides structure for SQLite3 database creation.

## Running the Project

1. Download source code from Github 💾
`git clone https://github.com/DogukanUrker/flaskBlog.git`

2. Go to directory 📁
`cd flaskBlog`

3. Install requirements.txt 🔽
`pip install -r requirements.txt`

It's ready to run 🎉
`python main.py`

### Default Admin Account

Email: admin@gmail.com
Password: admin

### Demo




