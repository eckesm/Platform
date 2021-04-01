from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request, flash, g

#####################################################################
# --------------------------- Admin View -------------------------- #
#####################################################################


# https://danidee10.github.io/2016/11/14/flask-by-example-7.html

class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):

        if "curr_user" not in session:
            return False
        elif g.user.role == 'administrator':
            return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():

            if "curr_user" not in session:
                flash("You must be logged-in to access this resource.", 'danger')
                return redirect('/login')
            else:
                flash("You are not authorized to access this resource.", 'danger')
                return redirect('/home')
