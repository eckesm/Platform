from flask import Flask, Blueprint, request, render_template, redirect, flash, session, make_response, jsonify, url_for, g
from flask import current_app as app
from sqlalchemy.sql import func
from ..auth.routes import log_out_procedures, restricted_group_privileges, restricted_not_authorized, CURR_USER_ID, login_required
from ..models import db, generate_random_string, Membership, Post, User, AWSFileStorage
from .. import forms
from .. import random_phrases
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware
from flask import send_from_directory
import os
from secrets import token_urlsafe
import boto3
import botocore
from botocore.exceptions import ClientError

users_bp = Blueprint(
    'users_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/users/static'
)

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config["S3_KEY"],
    aws_secret_access_key=app.config["S3_SECRET"]
)


def upload_file_to_s3(file, bucket_name, new_filename, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            new_filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(app.config["S3_LOCATION"], new_filename)

#####################################################################
# ------------------------- User Profiles ------------------------- #
#####################################################################


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@users_bp.route('/home')
def show_users_route():
    """Redirects to logged-in user's home page or the log in screen if not logged in."""

    if CURR_USER_ID not in session:
        return redirect('/')
    else:
        session['greeting'] = random_phrases.logged_in_home.get_phrase(
            f"{g.user.first_name}")
        return render_template('home.html')

# -------------------------------------------------------------------


@users_bp.route('/users/<username>')
def show_user_profile(username):

    user = User.get_user_by_username(username)

    if user == None:
        error = {'heading': 'User not found',
                 'message': f'There is no user matching the username {username}.'}
        return render_template('error.html', error=error)

    else:
        return render_template('profile.html', user=user)


#####################################################################
# ---------------------------- Edit User -------------------------- #
#####################################################################


@users_bp.route('/user/profile-picture', methods=['GET', 'POST'])
@login_required
def show_profile_picture_form():
    """Show form for user to change their profile picture."""

    user = g.user

    form = forms.ProfilePictureForm()
    if form.validate_on_submit():

        file = form.profile_url.data

        if allowed_file(file.filename) == False:
            flash("Selected file type is not permitted.", 'danger')
            return render_template('edit_profile_picture.html', form=form, user=user)

        if file and allowed_file(file.filename):

            original_filename, file_extension = os.path.splitext(file.filename)
            new_filename = generate_random_string(25,AWSFileStorage.get_file_by_id)
            output = upload_file_to_s3(file, app.config["S3_BUCKET"], f"{new_filename}{file_extension}")

            aws_url = output
            new_file = AWSFileStorage.add_file(
                new_filename, user.id, aws_url, 'image', 'profile-picture')

            user.profile_image_id = new_filename
            db.session.commit()

            return redirect('/user/profile-picture')

    return render_template('edit_profile_picture.html', form=form, user=user)


# -------------------------------------------------------------------

@ users_bp.route('/user/edit', methods=['GET', 'POST'])
@login_required
def update_user_profile():
    """Shows user profile form; attempts to edit the entered user information based on the form submission."""

    user = g.user

    form = forms.EditUserProfileForm(obj=user)
    if form.validate_on_submit():

        pronouns = form.pronouns.data
        subject_pronoun = form.subject_pronoun.data
        object_pronoun = form.object_pronoun.data

        if pronouns == 4:
            if subject_pronoun == '':
                subject_pronoun = None
            if object_pronoun == '':
                object_pronoun = None

        else:
            default_pronouns = retrieve_default_preferred_pronouns(pronouns)
            subject_pronoun = default_pronouns['subject']
            object_pronoun = default_pronouns['object']

        user.subject_pronoun = subject_pronoun
        user.object_pronoun = object_pronoun
        # user.profile_url = form.profile_url.data or User.profile_url.default.arg
        user.header_image_url = form.header_image_url.data or User.header_image_url.default.arg
        user.updated = func.now()
        db.session.commit()
        g.user = user

        session['greeting'] = random_phrases.logged_in_home.get_phrase(
            f"{g.user.first_name}")

        flash("Your account has been updated.", 'success')
        return redirect(f"/users/{g.user.username}")

    else:

        return render_template('edit_profile.html', user=user, form=form)


# -------------------------------------------------------------------


def retrieve_default_preferred_pronouns(pronouns):

    if pronouns == 1:
        return {'subject': 'he', 'object': 'him'}
    elif pronouns == 2:
        return {'subject': 'she', 'object': 'her'}
    else:
        return {'subject': 'they', 'object': 'them'}

# -------------------------------------------------------------------


@ users_bp.route('/user/delete', methods=['GET'])
@login_required
def delete_account_check():
    """Check that user definitely wants to delete their account."""

    return render_template('delete_account_check.html')

# -------------------------------------------------------------------


@ users_bp.route('/user/delete', methods=['POST'])
@login_required
def delete_account_confirm():
    """Delete user account and reroute to login screen."""

    user = g.user
    Membership.deactivate_memberships_by_member(user.id)
    Post.deactivate_post_by_owner(user.id)

    flash("Your account has been deleted.", 'danger')
    log_out_procedures()
    return redirect('/login')

# -------------------------------------------------------------------

# @users_bp.route('user/instagram', methods=['POST'])
# @login_required
# def show_instagram_portal():
#     import http.client

#     conn = http.client.HTTPSConnection("https://api.instagram.com/oauth/authorize")
#     headers={
#         client_id:"5205235132852224"

#     }
