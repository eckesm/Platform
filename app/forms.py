from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField, PasswordField, TextAreaField, FileField
from wtforms.validators import ValidationError, InputRequired, Optional, Email, EqualTo, URL, Length
import email_validator
from .models import User

PROHIBITED_USERNAMES = ['account', 'delete',
                        'edit', 'group', 'name', 'new', 'profile']

PERMITTED_NAME_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxyz-_'. "
PERMITTED_USERNAME_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxyz1234567890-_"
PERMITTED_PRONOUN_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxyz"
PERMITTED_PASSWORD_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqurstuvwxyz1234567890!@#$%^&*()-_+=;:?"


class PermittedChars(object):
    def __init__(self, permitted_characters, message=None):
        self.permitted_characters = permitted_characters
        if not message:
            message = f'Field can only contain the following characters: {permitted_characters}'
        self.message = message

    def __call__(self, form, field):
        for char in field.data:
            if char not in self.permitted_characters:
                raise ValidationError(self.message)


permittedchars = PermittedChars


def AvailableEmail(form, field):
    email = field.data
    if User.get_user_by_email(email) != None:
        raise ValidationError(
            f'The email address "{email}" is already associated with an account.')


def AvailableUsername(form, field):
    username = field.data
    if User.get_user_by_username(username) == None:
        if username in PROHIBITED_USERNAMES:
            raise ValidationError(f'The username "{username}" is prohibited')
    else:
        raise ValidationError(f'The username "{username}" is unavailable.')


def ActiveEmail(form, field):
    email = field.data
    user = User.get_user_by_email(email)
    if user == None:
        raise ValidationError(
            f'The email address "{email}" is not associated with an account.')
    elif user.status != 'active':
        raise ValidationError(
            f'The account associated with "{email}" has been deactivated.')


def ActiveUsername(form, field):
    username = field.data
    user = User.get_user_by_username(username)
    if user == None:
        raise ValidationError(
            f'The username "{username}" is not associated with an account.')
    elif user.status != 'active':
        raise ValidationError(
            f'The account associated with "{username}" has been deactivated.')


class AddUserForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField("First name", validators=[
                             InputRequired(message="Input required."),
                             Length(
                                 min=3, max=25, message="Must be between 3 and 25 characters."),
                             PermittedChars(permitted_characters=PERMITTED_NAME_CHARS, message="Names can only contain letters and -_'.")])
    last_name = StringField("Last name", validators=[
                            InputRequired(message="Input required."),
                            Length(
                                min=3, max=25, message="Must be between 3 and 25 characters."),
                            PermittedChars(permitted_characters=PERMITTED_NAME_CHARS, message="Names can only contain letters and -_'.")])
    username = StringField("Username", validators=[
                           InputRequired(message="Input required."),
                           Length(
                               min=6, max=25, message="Must be between 6 and 25 characters."),
                           PermittedChars(permitted_characters=PERMITTED_USERNAME_CHARS,
                                          message="Usernames can only contain letters and -_"),
                           AvailableUsername])
    email_address = StringField("Email address", validators=[
                                InputRequired(message="Input required."),
                                Email(
                                    message="Email address format required. Example: username@domain.com"),
                                AvailableEmail])
    password = PasswordField("Password", validators=[
                             InputRequired(message="Input required."),
                             Length(
                                 min=8, max=40, message="Must be between 8 and 40 characters."),
                             PermittedChars(permitted_characters=PERMITTED_PASSWORD_CHARS, message="Password can only contain letters, numbers, and !@#$%^&*()-_+=;:?")])

    agree_to_terms = BooleanField("Terms & Conditions", validators=[InputRequired(
        message="Must agree to terms and conditions to create account.")])


class PasswordResetForm(FlaskForm):
    """Form for resetting passwords via email."""

    email_address = StringField("Email address", validators=[
                                InputRequired(message="Input required."),
                                Email(
                                    message="Email address format required. Example: username@domain.com"), ActiveEmail])


class PasswordChangeForm(FlaskForm):
    """Form used to confirm that entered emails match."""

    email_address = StringField("Email address", validators=[
                                InputRequired(message="Input required."),
                                Email(
                                    message="Email address format required. Example: username@domain.com"), ActiveEmail])

    password = PasswordField("Password", validators=[
                             InputRequired(message="Input required."),
                             Length(
                                 min=8, max=40, message="Must be between 8 and 40 characters."),
                             PermittedChars(permitted_characters=PERMITTED_PASSWORD_CHARS,
                                            message="Password can only contain letters, numbers, and !@#$%^&*()-_+=;:?"),
                             EqualTo('confirm', message="The passwords must match.")])

    confirm = PasswordField("Enter password again")


class EditUserForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField("First name", validators=[
                             InputRequired(message="Input required."),
                             Length(
                                 min=3, max=25, message="Must be between 3 and 25 characters."),
                             PermittedChars(permitted_characters=PERMITTED_NAME_CHARS, message="Password can only contain letters and -_'.")])
    last_name = StringField("Last name", validators=[
                            InputRequired(message="Input required."),
                            Length(
                                min=3, max=25, message="Must be between 3 and 25 characters."),
                            PermittedChars(permitted_characters=PERMITTED_NAME_CHARS, message="Password can only contain letters and -_'.")])
    username = StringField("Username", validators=[
                           InputRequired(message="Input required."),
                           Length(
                               min=6, max=25, message="Must be between 6 and 25 characters."),
                           PermittedChars(permitted_characters=PERMITTED_USERNAME_CHARS,
                                          message="Password can only contain letters and -_")])
    email_address = StringField("Email address", validators=[
                                InputRequired(message="Input required."),
                                Email(
                                    message="Email address format required. Example: username@domain.com")])

    password = PasswordField("Password", validators=[
                             InputRequired(message="Please enter your current password to make changes to your account.")])


class EditUserProfileForm(FlaskForm):
    """Form for selecting preferred pronouns."""

    pronouns = RadioField("Preferred pronouns", choices=[
                          (1, 'he/him'), (2, 'she/her'), (3, 'they/them'), (4, 'other')], coerce=int)

    subject_pronoun = StringField("Subject pronoun", validators=[Optional(), Length(
        min=1, max=15, message="Must be between 1 and 15 characters."), PermittedChars(
        permitted_characters=PERMITTED_PRONOUN_CHARS, message="Pronouns can only contain letters.")])

    object_pronoun = StringField("Subject pronoun", validators=[Optional(), Length(
        min=1, max=15, message="Must be between 1 and 15 characters."), PermittedChars(permitted_characters=PERMITTED_PRONOUN_CHARS, message="Pronouns can only contain letters.")])

    # profile_url = StringField("Profile URL", validators=[
    #     Optional(), URL()])

    header_image_url = StringField("Heading image URL", validators=[
        Optional(), URL()])

class ProfilePictureForm(FlaskForm):
    profile_url = FileField("Profile Picture", validators=[InputRequired()])



class AddGroupForm(FlaskForm):
    """Form for creating a group."""

    name = StringField("Group name", validators=[InputRequired(message="Input required."), Length(
        min=1, max=100, message="Must be between 1 and 100 characters.")])
    description = TextAreaField("Description", validators=[Optional()])
    members_add_users = BooleanField(
        "Can regular members add new members to the group?")


class EditGroupForm(FlaskForm):
    """Form for editing a group."""

    name = StringField("Group name", validators=[InputRequired(message="Input required."), Length(
        min=1, max=100, message="Must be between 1 and 100 characters.")])
    description = TextAreaField("Description", validators=[Optional()])
    members_add_users = BooleanField(
        "Can regular members add new members to the group?")


class InviteToGroupForm(FlaskForm):
    """Form for inviting a user to a group."""

    username = StringField("Username", validators=[
                           InputRequired(message="Input required."), Length(
                               min=6, max=25, message="Must be between 6 and 25 characters."), ActiveUsername])


class LoginForm(FlaskForm):
    """User login form."""

    email_address = StringField("Email address", validators=[
        InputRequired(message="Input required."),
        Email(
            message="Email address format required. Example: username@domain.com")])

    password = PasswordField("Password", validators=[
                             InputRequired(message="Input required.")])


class PostForm(FlaskForm):
    """New post form."""

    content = StringField("Message", validators=[InputRequired()])
