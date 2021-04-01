from flask import Flask, Blueprint, request, render_template, redirect, flash, session, make_response, jsonify, url_for, g
from functools import wraps
from flask import current_app as app
from flask_mail import Mail, Message
from secrets import token_urlsafe
from sqlalchemy.sql import func
from ..models import db, User, Membership
from .. import forms
from .. import random_phrases
from os import environ

auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/auth/static'
)

mail = Mail(app)

# if app.config["ENV"] == "production":
#     app_url = secret.PRODUCTION_DOMAIN
# else:
#     app_url = 'http://127.0.0.1:5000'


app_url = app.config["PRODUCTION_DOMAIN"]

CURR_USER_ID = "curr_user"

@app.before_request
def add_user_to_g():
    """If logged in, add current user to Flask global."""

    if CURR_USER_ID in session:
        g.user = User.get_user_by_id(session[CURR_USER_ID])
        g.memberships = Membership.get_memberships_info_by_user_sorted(
            session[CURR_USER_ID])
        g.group_invitations = Membership.get_invitations_by_user_sorted(
            session[CURR_USER_ID])
    else:
        g.user = None
        g.memberships=None
        g.group_invitations=None

#####################################################################
# ----------------------- Access & Auxillary ---------------------- #
#####################################################################


def do_login(user):
    session[CURR_USER_ID] = user.id
    session.pop('new-user-entries', None)

def login_required(func):
    @wraps(func)
    def decorated_function(*args,**kwargs):
        if CURR_USER_ID not in session:
            log_out_procedures()
            flash("You must be logged-in to access this resource.", 'danger')
            return redirect(url_for('auth_bp.login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function


# -------------------------------------------------------------------


def restricted_not_authorized():
    flash("You are not authorized to access this resource.", 'danger')
    return redirect('/home')

# -------------------------------------------------------------------


def restricted_group_privileges(group_id):
    flash("Your group privileges do not allow you access this resource.", 'danger')
    return redirect(f'/groups/{group_id}')


#####################################################################
# -------------------------- Logging In --------------------------- #
#####################################################################


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Show login form on login.html page."""

    if CURR_USER_ID in session:
        flash('You have been logged out', 'info')
    log_out_procedures()

    form = forms.LoginForm()
    if form.validate_on_submit():
        email_address = form.email_address.data
        password = form.password.data
        user = User.authenticate(email_address, password)

        if user == None:
            flash(
                f'There is no user with the email address {email_address}.  Please make sure you are entering the correct email address with the correct spelling.', 'warning')
            return redirect('/login')

        if user == False:
            flash('Credentials entered were incorrect.  Please try again.',
                  'warning')
            return redirect('/login')

        if user:
            do_login(user)
            g.user = user

            flash('Login successful!', 'info')
            session['greeting'] = random_phrases.welcome_at_login.get_phrase(
                f"{g.user.first_name}")
            
            next_url = request.form.get("next")
            if next_url:
                return redirect(next_url)
            else:
                return redirect('/home')

    else:
        greeting = random_phrases.login_greetings.get_phrase()
        return render_template('login.html', greeting=greeting, form=form)


#####################################################################
# ------------------------- Logging Out --------------------------- #
#####################################################################


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Log out user."""
    if CURR_USER_ID not in session:
        flash('There is no user logged in.', 'info')
    else:
        flash('You have been logged out', 'info')
    log_out_procedures()
    return redirect('/login')

# -------------------------------------------------------------------


def log_out_procedures():

    if CURR_USER_ID in session:
        del session[CURR_USER_ID]

    session.pop('greeting', None)
    session.pop('new-user-entries', None)

    g.user = None
    g.memberships=None
    g.group_invitations=None


#####################################################################
# ---------------------- Register New User ------------------------ #
#####################################################################


@auth_bp.route('/register', methods=['GET', 'POST'])
def show_new_user_registration_form():
    """Attempts to create a new user based on form submission."""

    if CURR_USER_ID in session:
        flash('You have been logged out', 'info')
    log_out_procedures()

    form = forms.AddUserForm()
    if form.validate_on_submit():

        first_name = form.first_name.data
        last_name = form.last_name.data
        email_address = form.email_address.data
        username = form.username.data
        password = form.password.data
        agree_to_terms = form.agree_to_terms.data

        new_user = User.register(
            first_name, last_name, email_address, username, password)

        send_confirm_email_link(email_address)

        do_login(new_user)
        g.user=new_user

        session['greeting'] = random_phrases.welcome_first_login.get_phrase(
            f"{new_user.first_name}")
        return redirect('/home')

    else:
        greeting = random_phrases.new_user_greetings.get_phrase()
        return render_template('register.html', form=form, greeting=greeting)


#####################################################################
# ------------------ Edit/Delete Account Settings ----------------- #
#####################################################################


@auth_bp.route('/user/account', methods=['GET', 'POST'])
@login_required
def update_account_settings_from_form():
    """Attempts to edit the entered user account settings based on the form submission."""

    user = g.user
    current_email = user.email_address
    current_username = user.username

    form = forms.EditUserForm(obj=user)
    if form.validate_on_submit():

        password = form.password.data

        if user.authenticate(current_email, password) == None:
            flash("Entered password is incorrect.", 'danger')
            return render_template('edit_account_settings.html', form=form, current_email=current_email, current_username=current_username)

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data

        new_email = form.email_address.data
        new_username = form.username.data
        check_email = User.get_user_by_email(new_email)
        if check_email != None and check_email.email_address != current_email:
            flash(f"{new_email} is not available.", 'danger')
            return render_template('edit_account_settings.html', form=form, current_email=current_email, current_username=current_username)
        else:
            user.email_address = new_email

        if current_email != new_email:
            user.is_email_confirmed = False

        check_username = User.get_user_by_username(new_username)
        if check_username != None and check_username.username != current_username:
            flash(f"{new_username} is not available.", 'danger')
            return render_template('edit_account_settings.html', form=form, current_email=current_email, current_username=current_username)
        else:
            user.username = new_username

        user.updated = func.now()
        db.session.commit()
        g.user=user

        if current_email != new_email:
            send_confirm_email_link(new_email)

        session['greeting'] = random_phrases.logged_in_home.get_phrase(
            f"{user.first_name}")

        flash("Your account has been updated.", 'success')
        return redirect('/home')

    else:
        return render_template('edit_account_settings.html', form=form, current_email=current_email, current_username=current_username)


#####################################################################
# --------------------- Resetting Password ------------------------ #
#####################################################################

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if CURR_USER_ID in session:
        flash('You have been logged out', 'info')
    log_out_procedures()

    form = forms.PasswordResetForm()
    if form.validate_on_submit():
        email_address = form.email_address.data
        send_password_reset_link(email_address)
        return redirect('/login')
    else:
        return render_template('reset_password.html', form=form)

# -------------------------------------------------------------------


def send_password_reset_link(email_address):
    user = User.get_user_by_email(email_address)
    if user == None:
        flash('The entered email address is not associated with an account.', 'danger')
        return redirect('/reset-password')

    else:
        token = token_urlsafe(16)
        user.password_reset_token = token
        user.updated = func.now()
        db.session.commit()

        msg = Message('Need to reset your password?',
                      sender='eckesm@gmail.com',
                      recipients=[email_address])
        msg.body = f"Go to this link to reset your password: {app_url}/change-password/{token}"
        msg.html = f"<b>Don't fear!</b>  Help is on the way... Click <a href='{app_url}/change-password/{token}'>THIS LINK</a> to reset your password."
        mail.send(msg)
        flash('Check your email for a link to reset your password.', 'info')
        return

# -------------------------------------------------------------------


@auth_bp.route('/change-password/<token>', methods=['GET', 'POST'])
def change_password(token):
    """Show change password form and submit form."""
    
    if CURR_USER_ID in session:
        flash('You have been logged out', 'info')
    log_out_procedures()

    form = forms.PasswordChangeForm()
    if form.validate_on_submit():
        email_address = form.email_address.data
        user = User.get_user_by_email(email_address)

        if user.password_reset_token == None or user.password_reset_token != token:
            flash(f"This entered email address or token is incorrect.", 'danger')
            return render_template('change_password.html', form=form, token=token)

        if user.password_reset_token == token:
            password = form.password.data
            user.change_password(password)
            user.password_reset_token = None
            user.api_token=User.generate_api_token()
            user.updated = func.now()
            db.session.commit()
            flash('Your password has been updated.  Please log in again.', 'info')
            return redirect('/login')
    else:
        return render_template('change_password.html', form=form, token=token)


#####################################################################
# ------------------ Confirming Email Address --------------------- #
#####################################################################

def send_confirm_email_link(email_address):
    user = User.get_user_by_email(email_address)
    if user == None:
        flash('The entered email address is not associated with an account.', 'danger')
        log_out_procedures()
        return redirect('/login')

    else:
        token = token_urlsafe(16)
        user.email_confirm_token = token
        user.updated = func.now()
        db.session.commit()

        msg = Message('Please confirm your email address.',
                      sender='eckesm@gmail.com',
                      recipients=[email_address])
        msg.body = f"Go to this link to confirm your email address: {app_url}/confirm-email/{token}"
        msg.html = f"<b>Amost done!</b>  Click <a href='{app_url}/confirm-email/{token}'>THIS LINK</a> to confirm your email address."
        mail.send(msg)
        flash('Please check your email for a link to confirm your email address.', 'info')
        return

# -------------------------------------------------------------------


@auth_bp.route('/confirm-email/<token>', methods=['GET', 'POST'])
def confirm_email_address(token):
    """Confirm user's email address."""

    if CURR_USER_ID in session:
        flash('You have been logged out', 'info')
    log_out_procedures()

    form = forms.LoginForm()
    if form.validate_on_submit():

        email_address = form.email_address.data
        password = form.password.data
        user = User.authenticate(email_address, password)

        if user == None:
            flash(
                f'There is no user with the email address {email_address}.  Please make sure you are entering the correct email address with the correct spelling.', 'warning')
            return render_template('login.html', form=form, token=token)

        elif user == False:
            flash('Credentials entered were incorrect.  Please try again.',
                  'warning')
            return render_template('login.html', form=form, token=token)

        else:
            user = User.get_user_by_email(email_address)
            if user.email_confirm_token == None or user.email_confirm_token != token:
                flash(f"This entered email address or token is incorrect.", 'danger')
                return render_template('login.html', form=form, token=token)

            if user.email_confirm_token == token:
                user.is_email_confirmed = True
                user.email_confirm_token = None
                user.updated = func.now()
                db.session.commit()
                g.user=user
                flash('Your email address has been confirmed.', 'info')

                session['greeting'] = "Feels great to have that email address confirmed, amiright???"
                return redirect('/home')

    else:
        return render_template('login.html', form=form, token=token)
