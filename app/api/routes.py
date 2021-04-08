from flask import Flask, Blueprint, request, render_template, redirect, flash, session, make_response, jsonify, url_for
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask import current_app as app
from sqlalchemy.sql import func
from email_validator import validate_email, EmailNotValidError
import requests
from ..auth.routes import jwt
from ..forms import PROHIBITED_USERNAMES
from ..models import db, Group, Membership, User


# Blueprint configuration
api_bp = Blueprint(
    'api_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


#####################################################################
# --------------------------- API Requests ------------------------ #
#####################################################################


@ api_bp.route('/api/check-email', methods=['GET'])
def check_for_email_address():
    """Responds to js axios request with availability of entered email address."""

    email = request.args['email_address']

    try:
        # Validate.
        valid = validate_email(email)

        # Update with the normalized form.
        email = valid.email

    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        # print(str(e))
        return jsonify({'valid': False, 'email_address': email})

    valid = True
    if User.get_user_by_email(email) == None:
        available = True
    else:
        available = False
    return jsonify({'valid': valid, 'available': available, 'email_address': email})


# -------------------------------------------------------------------

@ api_bp.route('/api/check-username', methods=['GET'])
def check_for_username():
    """Responds to js axios request with availability of entered username."""

    username = request.args['username']
    if User.get_user_by_username(username) == None:

        if username in PROHIBITED_USERNAMES:
            available = False
        else:
            available = True

    else:
        available = False

    return jsonify({'available': available, 'username': username})


# -------------------------------------------------------------------

# NEED TO ENFORCE SOME SORT OF AUTHENTICATION

# @ api_bp.route('/api/users/<int:member_id>/invitations', methods=['GET'])
# def get_all_invitations_by_api(member_id):
#     invitations = Membership.get_invitations_by_user_sorted(member_id)
#     return jsonify(invitations=invitations)

# -------------------------------------------------------------------

# NEED TO ENFORCE SOME SORT OF AUTHENTICATION

# @ api_bp.route('/api/invitations/<int:invite_id>', methods=['GET'])
# def get_invitation_by_api(invite_id):

#     invitation = Membership.get_invitation_by_invite(invite_id)
#     if invitation == None:
#         return jsonify(message=f"There is no active invitation with ID {invite_id}.")
#     else:
#         return jsonify(invitation=invitation.serialize_invitation())

# -------------------------------------------------------------------


@ api_bp.route('/api/invitations/<invite_id>', methods=['PATCH'])
@jwt_required()
def accept_group_invitation_by_api(invite_id):

    current_user = get_jwt_identity()
    user = User.get_by_id(current_user)

    invitation = Membership.get_invitation_by_invite(invite_id)
    if invitation == None:
        return jsonify(message=f"This is not a valid invalid invitation. [Invitation ID: {invite_id}]")

    if invitation.member_id != user.id:
        return jsonify(message=f"You are not authorized to respond to this invitation. [Invitation ID: {invite_id}]")

    else:
        reply = request.json['reply']
        member_name = invitation.member.full_name
        group_name = invitation.group.name
        if reply == "accept":
            invitation.member_type = 'member'
            invitation.joined = func.now()
            invitation.updated = func.now()
            db.session.commit()
            return jsonify({'status': "successful", 'message': f"You are now a member of {group_name}"})

        elif reply == "reject":
            invitation.member_type = 'rejected'
            invitation.updated = func.now()
            db.session.commit()
            return jsonify({'status': "successful", 'message': f"You declined the invitation to join {group_name}"})

        else:
            return jsonify({'status': "unsuccessful", 'message': f"The reply {reply} is not recognized."})

# -------------------------------------------------------------------

# SHOULD USE JWT WHEN REACT IS IMPLEMENTS (RATHER THAN API TOKEN SETTING NOW)


@ api_bp.route('/api/invitations', methods=['POST'])
def invite_member_to_group_by_api():

    api_token = request.json['api_token']

    invited_by_id = request.json['invited_by_id']
    invited_by = User.get_by_id(invited_by_id)
    if invited_by == None:
        data = {
            "status": "unsuccessful",
            "message": f"The inviting user cannot be found. [Invited by ID: {invited_by}]"
        }
        return jsonify(data)

    if invited_by.api_token != api_token:
        data = {
            "status": "unsuccessful",
            "message": "You are not authenticated and cannot issue invitations."
        }
        return jsonify(data)

    group_id = request.json['group_id']
    invited_by_membership = Membership.get_membership_by_user_group(
        invited_by_id, group_id)
    if invited_by_membership.can_invite() == False:
        data = {
            "status": "unsuccessful",
            "message": "You are not permitted to issue invitations based on the group invitation settings."
        }
        return jsonify(data)

    member_id = request.json['member_id']
    member = User.get_by_id(member_id)
    if member == None:
        data = {
            "status": "unsuccessful",
            "message": f"The invited user cannot be found. [Member ID: {member_id}]"
        }
        return jsonify(data)

    group = Group.get_by_id(group_id)
    if group == None:
        data = {
            "status": "unsuccessful",
            "message": f"The group cannot be found. [Group ID: {group_id}]"
        }
        return jsonify(data)

    existing_member = Membership.get_membership_by_user_group(
        member_id, group_id)
    if existing_member != None and existing_member.member_type in ['member', 'owner']:
        return jsonify({"status": "existing member",
                        "message": f"{existing_member.member.full_name} is already a member of {existing_member.group.name}",
                        "invitation": existing_member.serialize_invitation()})

    else:
        existing_invitation = Membership.get_invitation_by_member_group(
            member_id, group_id)
        if existing_invitation != None:
            return jsonify({"status": "existing pending invitation",
                            "message": f"There is already a pending invitation for {existing_invitation.member.full_name} to join {existing_invitation.group.name}",
                            "invitation": existing_invitation.serialize_invitation()})

        else:
            new_invitation = Membership.register(
                member_id=member_id, group_id=group_id, member_type='invited', invited_by_id=invited_by_id, joined=None)
            return jsonify({"status": "successful",
                            "message": f"{new_invitation.member.full_name} has been invited to {new_invitation.group.name}",
                            "invitation": new_invitation.serialize_invitation()})
