from flask import Flask, Blueprint, request, render_template, redirect, flash, session, make_response, jsonify, url_for, g
from flask import current_app as app
from sqlalchemy.sql import func
from ..auth.routes import restricted_group_privileges, restricted_not_authorized, CURR_USER_ID, login_required
from ..models import db, Membership, Post
from .. import forms


# Blueprint configuration
posts_bp = Blueprint(
    'posts_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/posts/static'
)

#####################################################################
# ---------------------------- Messages --------------------------- #
#####################################################################


@posts_bp.route('/groups/<group_id>/posts', methods=['POST'])
@login_required
def post_message_to_thread(group_id):

    form = forms.PostForm()
    if form.validate_on_submit():

        membership = Membership.get_membership_by_user_group(
            session[CURR_USER_ID], group_id)
        if membership == None or membership.member_type not in ['member', 'owner']:
            return restricted_not_authorized()

        else:
            content = form.content.data
            new_post = Post.register(
                owner_id=session[CURR_USER_ID], group_id=group_id, content=content)

    else:
        flash('Messages must be at least 1 character.', 'warning')

    return redirect(f"/groups/{group_id}")