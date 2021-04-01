from flask import Blueprint, flash, redirect, render_template, session, g
from flask import current_app as app
from ..auth.routes import CURR_USER_ID
from .. import random_phrases


# Blueprint configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/home/static'
)


#####################################################################
# ---------------------------- Root ------------------------------- #
#####################################################################


@home_bp.route('/')
def index():

    if CURR_USER_ID not in session:
        return render_template('index.html')
    else:
        session['greeting'] = random_phrases.logged_in_home.get_phrase(
            f"{g.user.first_name}")
        return redirect('/home')
