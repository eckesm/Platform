# from flask import current_app as app
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import requests
from secrets import token_urlsafe
import string
import random
from os import environ
import json


db = SQLAlchemy()
bcrypt = Bcrypt()


# def connect_db(app):
#     db.app = app


def generate_random_string(length, unique_callback):
    unique_string = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=length))
    while(unique_callback(unique_string) != None):
        unique_string = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=length))
    return unique_string


def generate_random_integer(length, unique_callback):
    unique_string = ''.join(random.choices(string.digits, k=length))
    while(unique_callback(unique_string) != None):
        unique_string = ''.join(random.choices(string.digits, k=length))
    return int(unique_string)


class Scorecard(db.Model):
    """Scorecard for Eurovision votes."""

    __bind_key__ = 'eurovision_app'
    __tablename__ = 'scorecards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=True)

# class AppPrivileges(db.Model):

#     __tablename__='app_privileges'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
#     app_id=db.Column(db.Integer, db.ForeignKey('app.id'))
#     created=db.Column(db.DateTime, nullable=False, default=func.now())
#     updated=db.Column(db.DateTime, nullable=False, default=func.now())
#     status=db.Column(db.String(25), nullable=False, default='active')


class User(db.Model):
    """User model for users table."""

    # DEFAULT_PROFILE_URL='https://mre-platform.s3.us-east-2.amazonaws.com/default_user_profile_image'
    DEFAULT_PROFILE_URL = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi0.wp.com%2Fwww.repol.copl.ulaval.ca%2Fwp-content%2Fuploads%2F2019%2F01%2Fdefault-user-icon.jpg&f=1&nofb=1'

    DEFAULT_HEADER_IMAGE_URL = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fvastphotos.com%2Ffiles%2Fuploads%2Fphotos%2F10446%2Fcozy-winter-scene-l.jpg&f=1&nofb=1'

    __tablename__ = 'users'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(25), primary_key=True)
    email_address = db.Column(db.String(254), nullable=False, unique=True)
    email_confirm_token = db.Column(db.Text)
    is_email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    password_reset_token = db.Column(db.Text)
    api_token = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    subject_pronoun = db.Column(db.String(15), nullable=False, default='they')
    object_pronoun = db.Column(db.String(15), nullable=False, default='them')
    profile_image_id = db.Column(db.Text, nullable=False,
                                 default='default_user_profile_image')
    header_image_url = db.Column(
        db.Text, nullable=False, default=DEFAULT_HEADER_IMAGE_URL)
    created = db.Column(db.DateTime, nullable=False, default=func.now())
    updated = db.Column(db.DateTime, nullable=False, default=func.now())
    role = db.Column(db.Text, nullable=False, default='general')
    app_privileges = db.Column(db.Text, nullable=True, default=None)
    status = db.Column(db.Text, nullable=False, default='active')

    groups_owner = db.relationship('Group', backref='owner',
                                   cascade='all, delete-orphan')
    memberships = db.relationship('Membership', backref='member',
                                  cascade='all, delete-orphan')
    posts_own = db.relationship('Post', backref='owner',
                                cascade='all, delete-orphan')
    comments_own = db.relationship('Comment', backref='owner',
                                   cascade='all, delete-orphan')

    groups = db.relationship(
        'Group', secondary='memberships', backref='members')
    posts_view = db.relationship(
        'Post', secondary='groups', backref='viewers')

    @ property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # @full_name.setter
    # def full_name(self, name):
    #     first_name, last_name = name.split()
    #     self.first_name = first_name
    #     self.last_name = last_name

    # @full_name.deleter
    # def full_name(self):
    #     self.first_name = None
    #     self.last_name = None

    @ property
    def profile_image_url(self):
        if self.profile_image_id == 'default_user_profile_image':
            return User.DEFAULT_PROFILE_URL
        else:
            file = AWSFileStorage.get_file_by_id(self.profile_image_id)
            return file.url

    @ property
    def pronouns(self):
        pronouns = f"{self.subject_pronoun}/{self.object_pronoun}"
        if pronouns != 'he/him' and pronouns != 'she/her' and pronouns != 'they/them':
            return 'other'
        else:
            return pronouns

    def __repr__(Self):
        u = Self
        return f"<User id={u.id} | name={u.full_name}| username={u.username} | email={u.email_address} | pronouns={u.subject_pronoun}/{u.object_pronoun}>"

    # def get_serialized_safe_user_info(self):
    #     return {
    #         'id': self.id,
    #         'email_address': self.email_address,
    #         'username': self.username,
    #         'first_name': self.first_name,
    #         'last_name': self.last_name,
    #         'full_name': self.full_name,
    #         'subject_pronoun': self.subject_pronoun,
    #         'object_pronoun': self.object_pronoun,
    #         'pronouns': self.pronouns,
    #         'profile_image_url': self.profile_image_url,
    #         'created': self.created,
    #         'role': self.role
    #     }

    def change_password(self, password):
        """Change password."""
        hashed = bcrypt.generate_password_hash(password, rounds=14)
        self.password = hashed.decode("utf8")

    def get_app_privileges(self):
        if self.app_privileges:
            return json.loads(self.app_privileges)
        else:
            return None

    @ classmethod
    def generate_api_token(cls):
        return token_urlsafe(16)

    @ classmethod
    def register(cls, first_name, last_name, email_address, username, password):
        """Register a new user to the database."""
        hashed = bcrypt.generate_password_hash(password, rounds=14)
        hashed_utf = hashed.decode("utf8")

        new_user = cls(id=generate_random_string(25, cls.get_by_id), first_name=first_name, last_name=last_name, email_address=email_address.lower(
        ), username=username.lower(), password=hashed_utf, api_token=cls.generate_api_token())
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @ classmethod
    def authenticate(cls, email_address, password):
        """Validate that user exists and password is correct."""
        user = cls.query.filter_by(
            email_address=email_address.lower()).one_or_none()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                return cls.get_user_by_email(email_address.lower())
            else:
                return False
        else:
            return None

    @ classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).one_or_none()

    @ classmethod
    def get_user_by_email(cls, email_address):
        return cls.query.filter_by(email_address=email_address.lower()).one_or_none()

    @ classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username.lower()).one_or_none()

    @ classmethod
    def get_groups_by_id(cls, id):
        user = cls.query.get_or_404(id)
        return user.groups

    @ classmethod
    def get_full_name_by_id(cls, id):
        return cls.query.get_or_404(id).full_name


class Group(db.Model):
    """Group model for groups table."""

    __tablename__ = 'groups'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(25), primary_key=True)
    owner_id = db.Column(db.String(25), db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    members_add_users = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, nullable=False, default=func.now())
    updated = db.Column(db.DateTime, nullable=False, default=func.now())
    status = db.Column(db.String(25), nullable=False, default='active')

    memberships = db.relationship('Membership', backref='group',
                                  cascade='all, delete-orphan')
    posts = db.relationship('Post', backref='group',
                            cascade='all, delete-orphan')

    comments = db.relationship(
        'Comment', secondary='posts', backref='group')

    def __repr__(Self):
        g = Self
        return f"<Group id={g.id} | owner={g.owner.username} | name={g.name}>"

    def get_can_invite_list(self):
        can_invite_list = ['owner']
        if self.members_add_users == True:
            can_invite_list.append('member')
        return can_invite_list

    @classmethod
    def register(cls, owner_id, name, description, members_add_users):
        new_group = cls(id=generate_random_string(25, cls.get_by_id),
                        owner_id=owner_id, name=name, description=description, members_add_users=members_add_users)
        db.session.add(new_group)
        db.session.commit()
        return new_group

    @ classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).one_or_none()

    @ classmethod
    def get_members_by_id(cls, group_id):
        group = cls.query.get_or_404(group_id)
        return group.members

    @ classmethod
    def get_owner_by_id(cls, group_id):
        group = cls.query.get_or_404(group_id)
        return group.owner

    @ classmethod
    def get_safe_group(cls, group_id):

        group = cls.get_by_id(group_id)
        return {
            'id': group.id,
            'owner_id': group.owner_id,
            'name': group.name,
            'description': group.description,
            'members_add_users': group.members_add_users,
            'can_invite_list': group.get_can_invite_list()
        }


class Membership(db.Model):
    """Membership model for memberships table.  This table contains information linking users to groups."""

    __tablename__ = 'memberships'

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(25), primary_key=True)
    member_id = db.Column(db.String(25), db.ForeignKey(
        'users.id'), nullable=False)
    group_id = db.Column(db.String(25), db.ForeignKey(
        'groups.id'), nullable=False)
    member_type = db.Column(db.Text, nullable=False, default='invited')
    invited = db.Column(db.DateTime, nullable=False, default=func.now())
    # can this be a foreign key???
    invited_by_id = db.Column(db.String(25), nullable=False)
    joined = db.Column(db.DateTime)
    created = db.Column(db.DateTime, nullable=False, default=func.now())
    updated = db.Column(db.DateTime, nullable=False, default=func.now())
    status = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        m = self
        return f"<Membership user={m.member.username}| group={m.group.name} | type={m.member_type}>"

    def serialize_invitation(self):
        """Returns a dict representation of some membership data."""
        return {
            'id': self.id,
            'member_id': self.member_id,
            'member_name': self.member.full_name,
            'group_id': self.group_id,
            'group_name': self.group.name,
            'member_type': self.member_type,
            'invited': self.invited,
            'invited_by_id': self.invited_by_id,
            'invited_by_name': User.get_full_name_by_id(self.invited_by_id),
            'joined': self.joined
        }

    @classmethod
    def register(cls, member_id, group_id, member_type, invited_by_id, joined):
        new_membership = cls(id=generate_random_string(25, cls.get_by_id),
                             member_id=member_id, group_id=group_id, member_type=member_type, invited_by_id=invited_by_id, joined=joined)
        db.session.add(new_membership)
        db.session.commit()
        return new_membership

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).one_or_none()

    @ classmethod
    def get_serialized_safe_members_info_by_group_sorted(cls, group_id):
        members = db.session.query(Membership).filter(Membership.group_id == group_id, Membership.member_type.in_(
            ['invited', 'member', 'owner']), Membership.status == True).join(User).order_by(User.last_name, User.first_name).all()
        safe_members_info = []
        for member in members:
            safe_member_info = {
                'username': member.member.username,
                'first_name': member.member.first_name,
                'last_name': member.member.last_name,
                'full_name': member.member.full_name,
                'profile_image_url': member.member.profile_image_url,
                'member_type': member.member_type}
            safe_members_info.append(safe_member_info)
        return safe_members_info

    @ classmethod
    def get_memberships_info_by_user_sorted(cls, user_id):
        return db.session.query(Group.id, Group.name, Membership.member_type).filter(
            Membership.member_id == user_id, Membership.status == True).join(Membership).filter(Membership.member_type.in_(['owner', 'member'])).order_by(Group.name).all()

    @ classmethod
    def get_membership_by_user_group(cls, user_id, group_id):
        return Membership.query.filter(
            Membership.member_id == user_id, Membership.group_id == group_id, Membership.member_type.in_(['invited', 'member', 'owner']), Membership.status == True).one_or_none()

    @ classmethod
    def get_invitation_by_invite(cls, invite_id):
        return Membership.query.filter(Membership.id == invite_id, Membership.member_type == 'invited', Membership.status == True).one_or_none()

    @ classmethod
    def get_invitation_by_member_group(cls, member_id, group_id):
        return Membership.query.filter(Membership.member_id == member_id, Membership.group_id == group_id, Membership.member_type == 'invited', Membership.status == True).one_or_none()

    @ classmethod
    def get_invitations_by_user_sorted(csl, user_id):
        invitations = db.session.query(Membership).filter(
            Membership.member_id == user_id, Membership.member_type == 'invited', Membership.status == True).join(Group).order_by(Group.name).all()
        return [invitation.serialize_invitation() for invitation in invitations]

    # @classmethod
    # def invite_by_api(cls, member_id, group_id, invited_by_id, api_token, app_url):
    #     API_URL = f"{app_url}/api/invitations"
    #     json_data = {"member_id": member_id, "group_id": group_id,
    #                  "invited_by_id": invited_by_id, "api_token":api_token}
    #     response = requests.post(API_URL, json=json_data, headers={
    #                              "Content-Type": "application/json"})
    #     return response.json()

    @ classmethod
    def deactivate_memberships_by_member(cls, member_id):
        memberships = cls.query.filter_by(member_id=member_id).all()
        for membership in memberships:
            membership.status = False
        db.session.commit()


class Post(db.Model):
    """Post model for posts table."""

    __tablename__ = 'posts'

    # id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(25), primary_key=True)
    owner_id = db.Column(db.String(25), db.ForeignKey('users.id'))
    group_id = db.Column(db.String(25), db.ForeignKey('groups.id'))
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=func.now())
    updated = db.Column(db.DateTime, nullable=False, default=func.now())
    status = db.Column(db.String(25), nullable=False, default='active')

    @ property
    def friendly_datetime(self):
        return self.created.strftime("%A %#m/%#d/%Y %#I:%M:%S %p")

    @classmethod
    def register(cls, owner_id, group_id, content):
        new_post = cls(id=generate_random_string(25, cls.get_by_id),
                       owner_id=owner_id, group_id=group_id, content=content)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).one_or_none()

    @ classmethod
    def get_serialized_safe_posts(cls, joined, group_id):

        posts = cls.query.filter(
            Post.group_id == group_id, Post.created >= joined).order_by(Post.created).all()

        safe_posts = []
        for post in posts:
            safe_post = {
                'post_id': post.id,
                'post_content': post.content,
                'post_created': post.created,
                'post_status': post.status,
                'friendly_datetime': post.friendly_datetime
            }

            if post.status == 'active':
                safe_post['owner_id'] = post.owner.id
                safe_post['username'] = post.owner.username
                safe_post['first_name'] = post.owner.first_name
                safe_post['last_name'] = post.owner.last_name
                safe_post['full_name'] = post.owner.full_name
                safe_post['profile_image_url'] = post.owner.profile_image_url

            elif post.status == 'anonymous':
                safe_post['first_name'] = 'anonymous'
                safe_post['last_name'] = 'anonymous'
                safe_post['full_name'] = 'anonymous'
                safe_post['profile_image_url'] = User.DEFAULT_USER_URL

            safe_posts.append(safe_post)
        safe_posts.reverse()
        return safe_posts

    @ classmethod
    def deactivate_post_by_owner(cls, owner_id):
        posts = cls.query.filter_by(owner_id=owner_id).all()
        for post in posts:
            post.status = 'anonymous'
        db.session.commit()


class CommentType(db.Model):
    """CommentType model for comment_types table."""

    __tablename__ = 'comment_types'

    id = db.Column(db.String(25), primary_key=True)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=func.now())
    status = db.Column(db.String(25), nullable=False, default='active')


class Comment(db.Model):
    """Comment model for comments table."""

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.String(25), db.ForeignKey('users.id'))
    post_id = db.Column(db.String(25), db.ForeignKey('posts.id'))
    type_id = db.Column(db.String(50), db.ForeignKey('comment_types.id'))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=func.now())
    updated = db.Column(db.DateTime, nullable=False, default=func.now())
    status = db.Column(db.String(25), nullable=False, default='active')


class AWSFileStorage(db.Model):
    """Model for registering file in AWS S3 data lake."""

    __tablename__ = 'aws_file_storage'

    id = db.Column(db.String(25), primary_key=True)
    owner_id = db.Column(db.String(25), db.ForeignKey('users.id'))
    url = db.Column(db.Text, nullable=False)
    file_type = db.Column(db.String(25), nullable=False)
    category = db.Column(db.String(25), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=func.now())
    status = db.Column(db.String(25), nullable=False, default='active')

    @ classmethod
    def get_file_by_id(cls, file_id):
        return cls.query.filter_by(id=file_id).one_or_none()

    @ classmethod
    def add_file(cls, file_id, owner_id, url, file_type, category):
        """Add file to AWS File Storage model."""
        new_file = cls(id=file_id, owner_id=owner_id, url=url,
                       file_type=file_type, category=category)
        db.session.add(new_file)
        db.session.commit()
        return new_file
