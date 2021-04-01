from flask import Flask, Blueprint, request, render_template, redirect, flash, session, make_response, jsonify, url_for, g
from flask import current_app as app
from sqlalchemy.sql import func
from ..auth.routes import restricted_group_privileges, restricted_not_authorized, CURR_USER_ID, login_required
from ..models import db, Group, Membership, Post, User
from .. import forms
from .. import random_phrases
# from .. import secret
import requests


# Blueprint configuration
groups_bp = Blueprint(
    'groups_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/groups/static'
)

# if app.config["ENV"] == "production":
#     app_url = secret.PRODUCTION_DOMAIN
# else:
#     app_url = 'http://127.0.0.1:5000'

app_url = app.config["PRODUCTION_DOMAIN"]

#####################################################################
# --------------------------- Add Group --------------------------- #
#####################################################################

@ groups_bp.route('/group/new', methods=['GET', 'POST'])
@login_required
def attempt_new_group():

    form = forms.AddGroupForm()
    if form.validate_on_submit():

        name = form.name.data
        description = form.description.data
        if description == '':
            description = None
        members_add_users = form.members_add_users.data

        new_group = Group(
            owner_id=session[CURR_USER_ID],
            name=name,
            description=description,
            members_add_users=members_add_users
        )
        db.session.add(new_group)
        db.session.commit()

        new_membership = Membership(
            member_id=session[CURR_USER_ID],
            group_id=new_group.id,
            member_type='owner',
            invited_by_id=session[CURR_USER_ID],
            joined=func.now()
        )
        db.session.add(new_membership)
        db.session.commit()

        g.memberships = Membership.get_memberships_info_by_user_sorted(
            session[CURR_USER_ID])

        flash(
            f'Your group {new_group.name} has been created.', 'success')
        return redirect(f'/groups/{new_group.id}/invite')

    else:

        greeting = random_phrases.new_group_greeting.get_phrase()
        return render_template('new_group.html', greeting=greeting, form=form)


#####################################################################
# ----------------------- View Group Profile ---------------------- #
#####################################################################


@ groups_bp.route('/groups/<int:group_id>')
@login_required
def show_group_profile(group_id):

    membership = Membership.get_membership_by_user_group(session[CURR_USER_ID], group_id)

    if membership == None or membership.member_type not in ['invited', 'owner', 'member']:
        return restricted_not_authorized()

    else:
        form = forms.PostForm()
        member_type = membership.member_type
        safe_group = Group.get_safe_group(group_id)
        safe_members = Membership.get_serialized_safe_members_info_by_group_sorted(
            group_id)

        if member_type in ['owner', 'member']:
            safe_posts = Post.get_serialized_safe_posts(
                membership.joined, group_id)
        else:
            safe_posts = None

        return render_template('group_messages.html', form=form, group=safe_group, members=safe_members, posts=safe_posts, member_type=member_type)

#####################################################################
# ---------------------------- Edit Group ------------------------- #
#####################################################################


@ groups_bp.route('/groups/<int:group_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    """Show edit group form; submit edits to database."""

    membership = Membership.get_membership_by_user_group(
        session[CURR_USER_ID], group_id)
    if membership == None:
        return restricted_not_authorized()

    group = Group.get_group_by_id(group_id)
    if group.owner_id != session[CURR_USER_ID]:
        return restricted_group_privileges(group_id)

    else:

        form = forms.EditGroupForm(obj=group)
        if form.validate_on_submit():

            group.name = form.name.data
            group.description = form.description.data
            group.members_add_users = form.members_add_users.data
            group.updated=func.now()
            db.session.commit()

            flash(f'{group.name} has been updated.', 'success')
            return redirect(f'/groups/{group_id}')

        else:
            safe_group = Group.get_group_by_id(group_id)
            return render_template('edit_group.html', form=form, group=safe_group)


#####################################################################
# --------------------- Invite User to Group ---------------------- #
#####################################################################


@ groups_bp.route('/groups/<int:group_id>/invite', methods=['GET', 'POST'])
@login_required
def invite_user_to_group(group_id):
    """Show invitation form; add membership invitation to database."""

    membership = Membership.get_membership_by_user_group(
        session[CURR_USER_ID], group_id)
    if membership == None:
        return restricted_not_authorized()

    safe_group = Group.get_safe_group(group_id)
    member_type = membership.member_type

    if (member_type not in safe_group['can_invite_list']):
        return restricted_group_privileges(group_id)

    else:
        form = forms.InviteToGroupForm()
        if form.validate_on_submit():

            username = form.username.data
            invited_user = User.get_user_by_username(username)

            # invitation = Membership.invite_by_api(
            #     invited_user.id, group_id, session[CURR_USER_ID], g.user.api_token,app_url)

            API_URL = f"{app_url}/api/invitations"
            json_data = {
                "member_id": invited_user.id,
                "group_id": group_id,
                "invited_by_id": session[CURR_USER_ID],
                "api_token":g.user.api_token
                }
            response = requests.post(API_URL, json=json_data, headers={
                                 "Content-Type": "application/json"})
            invitation= response.json()

            status = invitation['status']
            message = invitation['message']
            
            if status=="successful":
                flash(message, 'success')
            else:
                flash(message, 'danger')

            safe_members = Membership.get_serialized_safe_members_info_by_group_sorted(
                group_id)

        else:
            safe_members = Membership.get_serialized_safe_members_info_by_group_sorted(
                group_id)

        return render_template('invite_to_group.html', form=form, group=safe_group, members=safe_members)
