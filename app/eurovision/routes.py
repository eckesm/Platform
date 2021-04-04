from flask import Flask, Blueprint, request, render_template, redirect, flash, session, make_response, jsonify, url_for, g
from flask import current_app as app
from sqlalchemy.sql import func
from functools import wraps
from ..auth.routes import restricted_group_privileges, restricted_not_authorized, CURR_USER_ID, login_required
from ..models import db, Group, Membership, Post, User, Application, ApplicationUser
from .. import forms
from .. import random_phrases
# from .. import secret
import requests
import json
import sys
from .forms import CountryForm, ParticipantForm, EntryForm, EventForm, EventEntryForm
import datetime
from os import environ


APPLICATION = Application.get_by_name('Eurovision API Manager')
APPLICATION_ID = APPLICATION.id
API_BASE_URL = environ.get('EUROVISION_API_BASE_URL')
API_KEY = environ.get('EUROVISION_API_KEY')
EVENT_TYPE_LIST = [('contest', 'Contest'), ('semi-final',
                                            'Semi-final'), ('final', 'Final')]

# Blueprint configuration
eurovision_bp = Blueprint(
    'eurovision_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/eurovision/static',
    url_prefix='/eurovision'
)



def eurovision_mgmt_authorization_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):

        
        app_user = ApplicationUser.get_active_appuser_by_ids(
            APPLICATION_ID, g.user.id)
        
        if app_user == None:
            flash('You do not have access to this resource.', 'danger')
            return redirect('/home')

        return func(*args, **kwargs)
    return decorated_function

# -------------------------------------------------------------------


def get_countries():
    response = requests.get(f"{API_BASE_URL}/countries")
    countries = response.json()['countries']
    return countries
# -------------------------------------------------------------------


def get_country(country_id):
    response = requests.get(f"{API_BASE_URL}/countries/{country_id}")
    country = response.json()['country']
    return country
# -------------------------------------------------------------------


def get_participants():
    response = requests.get(f"{API_BASE_URL}/participants")
    participants = response.json()['participants']
    return participants
# -------------------------------------------------------------------


def get_participant(participant_id):
    response = requests.get(f"{API_BASE_URL}/participants/{participant_id}")
    participant = response.json()['participant']
    return participant
# -------------------------------------------------------------------


def get_entries():
    response = requests.get(f"{API_BASE_URL}/entries")
    entries = response.json()['entries']
    return entries
# -------------------------------------------------------------------


def get_entry(entry_id):
    response = requests.get(f"{API_BASE_URL}/entries/{entry_id}")
    entry = response.json()['entry']
    return entry
# -------------------------------------------------------------------


def get_events():
    response = requests.get(f"{API_BASE_URL}/events")
    events = response.json()['events']
    return events
# -------------------------------------------------------------------


def get_event(event_id):
    response = requests.get(f"{API_BASE_URL}/events/{event_id}")
    event = response.json()['event']

    if event['date'] != None:
        datetime_obj = datetime.datetime.strptime(event['date'], '%d-%m-%Y')
        event['date'] = datetime_obj.date()
    return event
# -------------------------------------------------------------------


def get_performances():
    response = requests.get(f"{API_BASE_URL}/performances")
    performances = response.json()['performances']
    return performances
# -------------------------------------------------------------------


def get_performance(performance_id):
    response = requests.get(f"{API_BASE_URL}/performances/{performance_id}")
    performance = response.json()['performance']
    return performance

# -------------------------------------------------------------------


def form_error_message(errors):
    for error in errors:
        error_message = f"{error}: "
        for err in errors[error]:
            index = 0
            if index > 0:
                error_message += ', '
            error_message += err
            index += 1
        flash(error_message, 'danger')

# -------------------------------------------------------------------


@ eurovision_bp.route('/manage')
@login_required
@eurovision_mgmt_authorization_required
def show_eurovision_management():
    return redirect('/eurovision/manage/countries')


#####################################################################
# ------------------------- COUNTRIES ----------------------------- #
#####################################################################


@ eurovision_bp.route('/manage/countries')
@login_required
@eurovision_mgmt_authorization_required
def show_countries():

    form = CountryForm()
    countries = [(country['id'], country['country'])
                 for country in get_countries()]

    return render_template('country_form.html', countries=countries, form=form)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/countries/<country_id>')
@login_required
@eurovision_mgmt_authorization_required
def display_country(country_id):

    countries = [(country['id'], country['country'])
                 for country in get_countries()]
    selected_country = get_country(country_id)
    form = CountryForm()
    form.country_id.data = selected_country['id']
    form.country_name.data = selected_country['country']
    form.flag_image_url.data = selected_country['flag_image_url']

    return render_template('country_form.html', form=form, countries=countries, selected_country=selected_country)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/country/new', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def add_country():

    form = CountryForm()
    if form.validate_on_submit():

        country_id = request.form['country_id']
        country_name = request.form['country_name']
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        params = {
            "id": country_id,
            "country": country_name,
            "flag_image_url": request.form['flag_image_url']
        }

        response = requests.post(
            f"{API_BASE_URL}/countries", json=params, headers=headers)

        status = response.json()['status']
        if status == 'success':
            flash(f"{country_name} added successfully!", 'success')
        else:
            flash(f"There was an error adding {country_name}.", 'info')
        return redirect(f"/eurovision/manage/countries/{country_id.upper()}")

    else:
        form_error_message(form.errors)
        return render_template('country_form.html', form=form)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/countries/<country_id>/update', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def update_country(country_id):

    countries = [(country['id'], country['country'])
                 for country in get_countries()]

    selected_country = get_country(country_id)

    form = CountryForm()
    if form.validate_on_submit():

        country_name = request.form['country_name']
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        params = {
            "country": country_name,
            "flag_image_url": request.form['flag_image_url']
        }

        response = requests.put(
            f"{API_BASE_URL}/countries/{country_id}", json=params, headers=headers)

        status = response.json()['status']
        if status == 'success':
            flash(f"{country_name} updated successfully!", 'success')
        else:
            flash(f"There was an error updating {country_name}.", 'info')
        return redirect(f"/eurovision/manage/countries/{country_id}")

    else:
        form_error_message(form.errors)
        return render_template('country_form.html', form=form, countries=countries, selected_country=selected_country)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/countries/<country_id>/delete', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def delete_country(country_id):

    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }

    response = requests.delete(
        f"{API_BASE_URL}/countries/{country_id}", headers=headers)

    status = response.json()['status']
    if status == 'success':
        flash(f"{country_id} has been deleted!", 'success')
    else:
        flash(f"There was an error deleting {country_id}.", 'info')
    return redirect('/eurovision/manage/countries')

#####################################################################
# ------------------------ PARTICIPANTS --------------------------- #
#####################################################################


@ eurovision_bp.route('/manage/participants')
@login_required
@eurovision_mgmt_authorization_required
def show_participants():

    form = ParticipantForm()
    participants = [(participant['id'], participant['name'])
                    for participant in get_participants()]

    return render_template('participant_form.html', form=form, participants=participants)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/participants/<participant_id>')
@login_required
@eurovision_mgmt_authorization_required
def display_participant(participant_id):

    participants = [(participant['id'], participant['name'])
                    for participant in get_participants()]
    selected_participant = get_participant(participant_id)
    form = ParticipantForm()
    form.name.data = selected_participant['name']
    form.image_url.data = selected_participant['image_url']
    form.description.data = selected_participant['description']

    return render_template('participant_form.html', form=form, participants=participants, selected_participant=selected_participant)


# -------------------------------------------------------------------


@eurovision_bp.route('/manage/participant/new', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def add_participant():

    form = ParticipantForm()
    if form.validate_on_submit():

        participant_name = request.form['name']
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        params = {
            "name": participant_name,
            "image_url": request.form['image_url'],
            "description": request.form['description']
        }

        response = requests.post(
            f"{API_BASE_URL}/participants", json=params, headers=headers)

        status = response.json()['status']
        participant_id = response.json()['participant']['id']
        if status == 'success':
            flash(f"{participant_name} added successfully!", 'success')
        else:
            flash(f"There was an error adding {participant_name}.", 'info')
        return redirect(f"/eurovision/manage/participants/{participant_id}")

    else:
        form_error_message(form.errors)
        return render_template('participant_form.html', form=form)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/participants/<participant_id>/update', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def update_participant(participant_id):

    participants = [(participant['id'], participant['name'])
                    for participant in get_participants()]

    selected_participant = get_participant(participant_id)

    form = ParticipantForm()
    if form.validate_on_submit():

        participant_name = request.form['name']
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        params = {
            "name": participant_name,
            "image_url": request.form['image_url'],
            "description": request.form['description']
        }

        response = requests.put(
            f"{API_BASE_URL}/participants/{participant_id}", json=params, headers=headers)

        status = response.json()['status']
        if status == 'success':
            flash(f"{participant_name} updated successfully!", 'success')
        else:
            flash(f"There was an error updating {participant_name}.", 'info')
        return redirect(f"/eurovision/manage/participants/{participant_id}")

    else:
        form_error_message(form.errors)
        return render_template('participant_form.html', form=form, participants=participants, selected_participant=selected_participant)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/participants/<participant_id>/delete', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def delete_participant(participant_id):

    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }
    response = requests.delete(
        f"{API_BASE_URL}/participants/{participant_id}", headers=headers)

    status = response.json()['status']
    if status == 'success':
        flash(f"{participant_id} has been deleted!", 'success')
    else:
        flash(f"There was an error deleting {participant_id}.", 'info')
    return redirect('/eurovision/manage/participants')

#####################################################################
# ---------------------------- ENTRIES ---------------------------- #
#####################################################################


@ eurovision_bp.route('/manage/entries')
@login_required
@eurovision_mgmt_authorization_required
def show_entries():

    entries = [(entry['id'], entry['title']) for entry in get_entries()]
    participants = [(participant['id'], participant['name'])
                    for participant in get_participants()]
    countries = [(country['id'], country['country'])
                 for country in get_countries()]

    form = EntryForm()

    return render_template('entry_form.html', form=form, entries=entries, participants=participants, countries=countries)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/entries/<entry_id>')
@login_required
@eurovision_mgmt_authorization_required
def display_entry(entry_id):

    entries = [(entry['id'], entry['title']) for entry in get_entries()]
    participants = [(participant['id'], participant['name'])
                    for participant in get_participants()]
    countries = [(country['id'], country['country'])
                 for country in get_countries()]

    selected_entry = get_entry(entry_id)
    form = EntryForm()
    form.participant_id.data = selected_entry['participant_id']
    form.country_id.data = selected_entry['country_id']
    form.title.data = selected_entry['title']
    form.year.data = selected_entry['year']
    form.eurovision_resource_url.data = selected_entry['eurovision_resource_url']
    form.eurovision_video_url.data = selected_entry['eurovision_video_url']
    form.music_video_url.data = selected_entry['music_video_url']
    form.spotify_url.data = selected_entry['spotify_url']
    form.written_by.data = selected_entry['written_by']
    form.composed_by.data = selected_entry['composed_by']
    form.broadcaster.data = selected_entry['broadcaster']
    form.lyrics.data = selected_entry['lyrics']
    form.lyrics_language.data = selected_entry['lyrics_language']
    form.lyrics_english.data = selected_entry['lyrics_english']

    return render_template('entry_form.html', form=form, entries=entries, participants=participants, countries=countries, selected_entry=selected_entry)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/entry/new', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def add_entry():

    entries = [(entry['id'], entry['title']) for entry in get_entries()]
    participants = [(participant['id'], participant['name'])
                    for participant in get_participants()]
    countries = [(country['id'], country['country'])
                 for country in get_countries()]

    form = EntryForm()
    form.participant_id.choices = participants
    form.country_id.choices = countries
    if form.validate_on_submit():

        entry_name = request.form['title']
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        params = {
            "participant_id": request.form['participant_id'],
            "country_id": request.form['country_id'],
            "title": entry_name,
            "year": request.form['year'],
            "eurovision_resource_url": request.form['eurovision_resource_url'],
            "eurovision_video_url": request.form['eurovision_video_url'],
            "music_video_url": request.form['music_video_url'],
            "spotify_url": request.form['spotify_url'],
            "written_by": request.form['written_by'],
            "composed_by": request.form['composed_by'],
            "broadcaster": request.form['broadcaster'],
            "lyrics": request.form['lyrics'],
            "lyrics_language": request.form['lyrics_language'],
            "lyrics_english": request.form['lyrics_english']
        }

        response = requests.post(
            f"{API_BASE_URL}/entries", json=params, headers=headers)

        status = response.json()['status']
        entry_id = response.json()['entry']['id']
        if status == 'success':
            flash(f"{entry_name} added successfully!", 'success')
        else:
            flash(f"There was an error adding {entry_name}.", 'info')
        return redirect(f"/eurovision/manage/entries/{entry_id}")

    else:
        form_error_message(form.errors)
        return render_template('entry_form.html', entries=entries, form=form, participants=participants, countries=countries)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/entries/<entry_id>/update', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def update_entry(entry_id):

    entries = [(entry['id'], entry['title']) for entry in get_entries()]
    participants = [(participant['id'], participant['name'])
                    for participant in get_participants()]
    countries = [(country['id'], country['country'])
                 for country in get_countries()]

    form = EntryForm()
    form.participant_id.choices = participants
    form.country_id.choices = countries
    if form.validate_on_submit():

        entry_name = request.form['title']
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        params = {
            "participant_id": request.form['participant_id'],
            "country_id": request.form['country_id'],
            "title": entry_name,
            "year": request.form['year'],
            "eurovision_resource_url": request.form['eurovision_resource_url'],
            "eurovision_video_url": request.form['eurovision_video_url'],
            "music_video_url": request.form['music_video_url'],
            "spotify_url": request.form['spotify_url'],
            "written_by": request.form['written_by'],
            "composed_by": request.form['composed_by'],
            "broadcaster": request.form['broadcaster'],
            "lyrics": request.form['lyrics'],
            "lyrics_language": request.form['lyrics_language'],
            "lyrics_english": request.form['lyrics_english']
        }

        response = requests.put(
            f"{API_BASE_URL}/entries/{entry_id}", json=params, headers=headers)

        status = response.json()['status']
        if status == 'success':
            flash(f"{entry_name} updated successfully!", 'success')
        else:
            flash(f"There was an error updating {entry_name}.", 'info')
        return redirect(f"/eurovision/manage/entries/{entry_id}")

    else:
        form_error_message(form.errors)
        return render_template('entry_form.html', form=form, entries=entries, participants=participants, countries=countries, selected_entry=get_entry(entry_id))

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/entries/<entry_id>/delete', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def delete_entry(entry_id):

    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }

    response = requests.delete(
        f"{API_BASE_URL}/entries/{entry_id}", headers=headers)

    status = response.json()['status']
    if status == 'success':
        flash(f"{entry_id} has been deleted!", 'success')
    else:
        flash(f"There was an error deleting {entry_id}.", 'info')
    return redirect('/eurovision/manage/entries')

#####################################################################
# ------------------------- EVENTS ----------------------------- #
#####################################################################


@ eurovision_bp.route('/manage/events')
@login_required
@eurovision_mgmt_authorization_required
def show_events():

    events = [(event['id'], event['event'])
              for event in get_events()]
    countries = [(country['id'], country['country'])
                 for country in get_countries()]

    form = EventForm()
    form.host_country_id.choices = countries

    return render_template('event_form.html', form=form, events=events, types=EVENT_TYPE_LIST, countries=countries)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/events/<event_id>')
@login_required
@eurovision_mgmt_authorization_required
def display_event(event_id):

    events = [(event['id'], event['event'])
              for event in get_events()]
    countries = [(country['id'], country['country'])
                 for country in get_countries()]

    selected_event = get_event(event_id)
    form = EventForm()
    form.event_name.data = selected_event['event']
    form.type.data = selected_event['type']
    form.year.data = selected_event['year']
    form.date.data = selected_event['date']
    form.start_time.data = selected_event['start_time']
    form.end_time.data = selected_event['end_time']
    form.eurovision_resource_url.data = selected_event['eurovision_resource_url']
    form.recap_video_url.data = selected_event['recap_video_url']
    form.video_playlist_url.data = selected_event['video_playlist_url']
    form.spotify_playlist_url.data = selected_event['spotify_playlist_url']
    form.host_city.data = selected_event['host_city']
    form.host_country_id.data = selected_event['host_country_id']

    return render_template('event_form.html', form=form, events=events, types=EVENT_TYPE_LIST, countries=countries, selected_event=selected_event)


# -------------------------------------------------------------------


@eurovision_bp.route('/manage/event/new', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def add_event():

    events = [(event['id'], event['event'])
              for event in get_events()]
    countries = [(country['id'], country['country'])
                 for country in get_countries()]

    form = EventForm()
    form.type.choices = EVENT_TYPE_LIST
    form.host_country_id.choices = countries
    if form.validate_on_submit():

        event_name = request.form['event_name']
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        params = {
            "event": event_name,
            "type": request.form['type'],
            "year": request.form['year'],
            "date": request.form['date'],
            "start_time": request.form['start_time'],
            "end_time": request.form['end_time'],
            "eurovision_resource_url": request.form['eurovision_resource_url'],
            "recap_video_url": request.form['recap_video_url'],
            "video_playlist_url": request.form['video_playlist_url'],
            "spotify_playlist_url": request.form['spotify_playlist_url'],
            "host_city": request.form['host_city'],
            "host_country_id": request.form['host_country_id']
        }

        response = requests.post(
            f"{API_BASE_URL}/events", json=params, headers=headers)

        status = response.json()['status']
        event_id = response.json()['event']['id']
        if status == 'success':
            flash(f"{event_name} added successfully!", 'success')
        else:
            flash(f"There was an error adding {event_name}.", 'info')
        return redirect(f"/eurovision/manage/events/{event_id}")

    else:
        form_error_message(form.errors)
        return render_template('event_form.html', form=form, events=events, types=EVENT_TYPE_LIST, countries=countries)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/events/<event_id>/update', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def update_event(event_id):

    events = [(event['id'], event['event'])
              for event in get_events()]
    countries = [(country['id'], country['country'])
                 for country in get_countries()]

    form = EventForm()
    form.type.choices = EVENT_TYPE_LIST
    form.host_country_id.choices = countries
    if form.validate_on_submit():

        event_name = request.form['event_name']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        if not start_time:
            start_time = "12:00"
        if not end_time:
            end_time = "12:00"
        end_time = request.form['end_time']
        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        params = {
            "event": event_name,
            "type": request.form['type'],
            "year": request.form['year'],
            "date": request.form['date'],
            "start_time": start_time,
            "end_time": end_time,
            "eurovision_resource_url": request.form['eurovision_resource_url'],
            "recap_video_url": request.form['recap_video_url'],
            "video_playlist_url": request.form['video_playlist_url'],
            "spotify_playlist_url": request.form['spotify_playlist_url'],
            "host_city": request.form['host_city'],
            "host_country_id": request.form['host_country_id']
        }

        response = requests.put(
            f"{API_BASE_URL}/events/{event_id}", json=params, headers=headers)

        status = response.json()['status']
        if status == 'success':
            flash(f"{event_name} updated successfully!", 'success')
        else:
            flash(f"There was an error updating {event_name}.", 'info')
        return redirect(f"/eurovision/manage/events/{event_id}")

    else:
        form_error_message(form.errors)
        return render_template('event_form.html', form=form, events=events, countries=countries, selected_event=get_event(event_id))

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/events/<event_id>/delete', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def delete_event(event_id):

    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }

    response = requests.delete(
        f"{API_BASE_URL}/events/{event_id}", headers=headers)

    status = response.json()['status']
    if status == 'success':
        flash(f"{event_id} has been deleted!", 'success')
    else:
        flash(f"There was an error deleting {event_id}.", 'info')
    return redirect('/eurovision/manage/events')

#####################################################################
# ------------------------- PERFORMANCES -------------------------- #
#####################################################################


@ eurovision_bp.route('/manage/performances')
@login_required
@eurovision_mgmt_authorization_required
def show_performances():

    performances = [(performance['id'], f"{performance['entry']} | {performance['participant']} | {performance['country']}")
                    for performance in get_performances()]
    events = [(event['id'], event['event'])
              for event in get_events()]
    entries = [(entry['id'], f"{entry['title']} | {entry['participant']} | {entry['country']}")
               for entry in get_entries()]

    form = EventEntryForm()

    return render_template('performance_form.html', form=form, performances=performances, events=events, entries=entries)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/performances/<performance_id>')
@login_required
@eurovision_mgmt_authorization_required
def display_performance(performance_id):

    performances = [(performance['id'], f"{performance['entry']} | {performance['participant']} | {performance['country']}")
                    for performance in get_performances()]
    events = [(event['id'], event['event'])
              for event in get_events()]
    entries = [(entry['id'], f"{entry['title']} | {entry['participant']} | {entry['country']}")
               for entry in get_entries()]

    selected_performance = get_performance(performance_id)
    form = EventEntryForm()
    form.event_id.data = selected_performance['event_id']
    form.entry_id.data = selected_performance['entry_id']
    form.points.data = selected_performance['points']
    form.place.data = selected_performance['place']
    form.qualified.data = selected_performance['qualified']
    form.running_order.data = selected_performance['running_order']

    return render_template('performance_form.html', form=form, performances=performances, events=events, entries=entries, selected_performance=selected_performance)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/performance/new', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def add_performance():

    performances = [(performance['id'], f"{performance['entry']} | {performance['participant']} | {performance['country']}")
                    for performance in get_performances()]
    events = [(event['id'], event['event'])
              for event in get_events()]
    entries = [(entry['id'], f"{entry['title']} | {entry['participant']} | {entry['country']}")
               for entry in get_entries()]

    form = EventEntryForm()
    form.event_id.choices = events
    form.entry_id.choices = entries
    form.qualified.choices = [('true', 'Yes'), ('false', 'No')]
    if form.validate_on_submit():

        points = request.form['points']
        if points == '':
            points = 0

        place = request.form['place']
        if place == '':
            place = 0

        running_order = request.form['running_order']
        if running_order == '':
            running_order = 0

        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        params = {
            "event_id": request.form['event_id'],
            "entry_id": request.form['entry_id'],
            "points": points,
            "place": place,
            "qualified": request.form['qualified'],
            "running_order": running_order
        }

        response = requests.post(
            f"{API_BASE_URL}/performances", json=params, headers=headers)

        status = response.json()['status']
        performance_id = response.json()['performance']['id']
        if status == 'success':
            flash(f"{performance_id} added successfully!", 'success')
        else:
            flash(f"There was an error adding {performance_id}.", 'info')
        return redirect(f"/eurovision/manage/performances/{performance_id}")

    else:
        form_error_message(form.errors)
        return render_template('performance_form.html', form=form, performances=performances, events=events, entries=entries)

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/performances/<performance_id>/update', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def update_performance(performance_id):

    performances = [(performance['id'], f"{performance['entry']} | {performance['participant']} | {performance['country']}")
                    for performance in get_performances()]
    events = [(event['id'], event['event'])
              for event in get_events()]
    entries = [(entry['id'], f"{entry['title']} | {entry['participant']} | {entry['country']}")
               for entry in get_entries()]

    form = EventEntryForm()
    form.event_id.choices = events
    form.entry_id.choices = entries
    form.qualified.choices = [('true', 'Yes'), ('false', 'No')]
    if form.validate_on_submit():

        points = request.form['points']
        if points == '':
            points = 0

        place = request.form['place']
        if place == '':
            place = 0

        running_order = request.form['running_order']
        if running_order == '':
            running_order = 0

        headers = {
            'Content-Type': 'application/json',
            'API-Key': API_KEY
        }
        params = {
            "event_id": request.form['event_id'],
            "entry_id": request.form['entry_id'],
            "points": points,
            "place": place,
            "qualified": request.form['qualified'],
            "running_order": running_order
        }

        response = requests.put(
            f"{API_BASE_URL}/performances/{performance_id}", json=params, headers=headers)

        status = response.json()['status']
        if status == 'success':
            flash(f"{performance_id} updated successfully!", 'success')
        else:
            flash(f"There was an error updating {performance_id}.", 'info')
        return redirect(f"/eurovision/manage/performances/{performance_id}")

    else:
        form_error_message(form.errors)
        return render_template('performance_form.html', form=form, performances=performances, events=events, entries=entries, selected_performance=get_performance(performance_id))

# -------------------------------------------------------------------


@eurovision_bp.route('/manage/performances/<performance_id>/delete', methods=['GET', 'POST'])
@login_required
@eurovision_mgmt_authorization_required
def delete_performance(performance_id):

    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }

    response = requests.delete(
        f"{API_BASE_URL}/performances/{performance_id}", headers=headers)

    status = response.json()['status']
    if status == 'success':
        flash(f"{performance_id} has been deleted!", 'success')
    else:
        flash(f"There was an error deleting {performance_id}.", 'info')
    return redirect('/eurovision/manage/performances')
