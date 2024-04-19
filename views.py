from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditorField
from flask_login import current_user

from models import User, Post

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class UserAdmin(AdminModelView):
    column_list = ('first_name', 'last_name', 'username', 'email')
    column_labels = {'first_name': 'First name', 'last_name': 'Last name', 'username': 'Username', 'email': 'Email Address'}
    column_filters = ('username', 'email')


class PostAdmin(AdminModelView):
    column_list = ('title', 'content')
    form_overrides = dict(content=CKEditorField)
    column_labels = {'title': 'Post Title', 'content': 'Content'}
    create_template = 'edit.html'
    edit_template = 'edit.html'