#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String, nullable=True)
    website = db.Column(db.String, nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=True, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship('Shows', backref='venue', lazy=True, cascade="all, delete")


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String, nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=True, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship('Shows', backref='artist', lazy=True, cascade="all, delete")

class Shows(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete="CASCADE"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete="CASCADE"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  city_states = Venue.query.distinct(Venue.city, Venue.state).all()
  for cs in city_states:
    lst = []
    for v in Venue.query.filter(Venue.city == cs.city, Venue.state == cs.state).all():
      num_upcoming_shows =   Shows.query.filter(
        Shows.venue_id == v.id, 
        Shows.start_time >= datetime.now()
        ).count()
      v.num_upcoming_shows = num_upcoming_shows
      lst.append(v)
    dct = {
      'city': cs.city,
      'state': cs.state,
      'venues': lst,
      }
    data.append(dct)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '').lower()
  venues = Venue.query.filter(Venue.name.ilike("%{}%".format(search_term))).all()
  count = len(venues)
  data = []
  for venue in venues:
      num_upcoming_shows =   Shows.query.filter(
        Shows.venue_id == venue.id, 
        Shows.start_time >= datetime.now()
        ).count()
        
      data.append(
        {
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": num_upcoming_shows
          })
  response = {
    "count": count,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Venue.query.get(venue_id)
  try:
    data.genres = data.genres.strip('{}').split(',')
  except:
    pass
  
  past_shows_count = Shows.query.filter(
    Shows.venue_id == venue_id,
    Shows.start_time < datetime.now()
    ).count()

  upcoming_shows_count = Shows.query.filter(
    Shows.venue_id == venue_id,
    Shows.start_time >= datetime.now()
    ).count()
  
  past_shows = Shows.query.order_by(Shows.start_time).filter(
    Shows.venue_id == venue_id,
    Shows.start_time < datetime.now()).all()

  for show in past_shows:
    show.start_time = format_datetime(str(show.start_time))

  upcoming_shows = Shows.query.order_by(Shows.start_time).filter(
    Shows.venue_id == venue_id,
    Shows.start_time >= datetime.now()).all()

  for show in upcoming_shows:
    show.start_time = format_datetime(str(show.start_time))


  data.upcoming_shows = upcoming_shows
  data.past_shows = past_shows
  data.past_shows_count = past_shows_count
  data.upcoming_shows_count = upcoming_shows_count
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm()
  valid = form.validate()
  venue = Venue(
    name = form.data['name'],
    city = form.data['city'],
    state = form.data['state'],
    address = form.data['address'],
    phone = form.data['phone'],
    genres = form.data['genres'],
    facebook_link = form.data['facebook_link'],
    website = form.data['website'],
    image_link = form.data['image_link'],
    seeking_talent = form.data['seeking_talent'],
    seeking_description = form.data['seeking_description']
  )
  if valid:
    try:
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + form.data['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Venue ' + form.data['name'] + ' could not be inserted into the database.')
    finally:
      db.session.close()
  if not valid:
    flash('An error occurred. Venue ' + form.data['name'] + ' has an error in a field.')
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.distinct(Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '').lower()
  artists = Artist.query.filter(Artist.name.ilike("%{}%".format(search_term))).all()
  count = len(artists)
  data = []
  for artist in artists:
    num_upcoming_shows =   Shows.query.filter(
      Shows.artist_id == artist.id, 
      Shows.start_time >= datetime.now()
      ).count()

    data.append(
      {
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": num_upcoming_shows
        })
  response = {
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Artist.query.get(artist_id)
  try:
    data.genres = data.genres.strip('{}').split(',')
  except:
    pass

  past_shows_count = Shows.query.filter(
    Shows.artist_id == artist_id,
    Shows.start_time < datetime.now()
    ).count()

  upcoming_shows_count = Shows.query.filter(
    Shows.artist_id == artist_id,
    Shows.start_time >= datetime.now()
    ).count()
  
  past_shows = Shows.query.order_by(Shows.start_time).filter(
    Shows.artist_id == artist_id,
    Shows.start_time < datetime.now()).all()
  
  for show in past_shows:
    show.start_time = format_datetime(str(show.start_time))

  upcoming_shows = Shows.query.order_by(Shows.start_time).filter(
    Shows.artist_id == artist_id,
    Shows.start_time >= datetime.now()).all()

  for show in upcoming_shows:
    show.start_time = format_datetime(str(show.start_time))


  data.upcoming_shows = upcoming_shows
  data.past_shows = past_shows
  data.past_shows_count = past_shows_count
  data.upcoming_shows_count = upcoming_shows_count
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  valid = form.validate()
  if valid:
    try:
      artist = Artist.query.get(artist_id)
      artist.name = form.data['name']
      artist.city = form.data['city']
      artist.state = form.data['state']
      artist.phone = form.data['phone']
      artist.genres = form.data['genres']
      artist.facebook_link = form.data['facebook_link']
      artist.website = form.data['website']
      artist.image_link = form.data['image_link']
      artist.seeking_venue = form.data['seeking_venue']
      artist.seeking_description = form.data['seeking_description']
      db.session.commit()
      flash('Artist ' + form.data['name'] + ' was successfully updated!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist ' + form.data['name'] + ' could not be updated.')
    finally:
      db.session.close()
  if not valid:
    flash('An error occurred. Artist ' + form.data['name'] + ' has an error in a field.')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  valid = form.validate()
  if valid:
    try:
      venue = Venue.query.get(venue_id)
      venue.name = form.data['name']
      venue.city = form.data['city']
      venue.state = form.data['state']
      venue.address = form.data['address']
      venue.phone = form.data['phone']
      venue.genres = form.data['genres']
      venue.facebook_link = form.data['facebook_link']
      venue.website = form.data['website']
      venue.image_link = form.data['image_link']
      venue.seeking_talent = form.data['seeking_talent']
      venue.seeking_description = form.data['seeking_description']
      db.session.commit()
      flash('Venue ' + form.data['name'] + ' was successfully updated!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Venue ' + form.data['name'] + ' could not be updated.')
    finally:
      db.session.close()
  if not valid:
    flash('An error occurred. Venue ' + form.data['name'] + ' has an error in a field.')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm()
  valid = form.validate()
  artist = Artist(
    name=form.data['name'],
    city=form.data['city'],
    state=form.data['state'],
    phone=form.data['phone'],
    genres = form.data['genres'],
    facebook_link = form.data['facebook_link'],
    website = form.data['website'],
    image_link = form.data['image_link'],
    seeking_venue = form.data['seeking_venue'],
    seeking_description = form.data['seeking_description']
    )
  if valid:
    try:
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist ' + form.data['name'] + ' could not be inserted into the database.')
    finally:
      db.session.close()
  if not valid:
    flash('An error occurred. Artist ' + form.data['name'] + ' has an error in a field.')
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  try:
    artist = Artist.query.filter_by(id=artist_id).first()
    db.session.delete(artist)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })
  return None
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = Shows.query.order_by(Shows.start_time).all()
  for show in data:
    show.start_time = format_datetime(str(show.start_time))
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # TODO: insert form data as a new Show record in the db, instead

  form = ShowForm(request.form)
  valid = form.validate()
  show = Shows(
    artist_id=form.data['artist_id'],
    venue_id=form.data['venue_id'],
    start_time=form.data['start_time']
  )
  if valid:
    try:
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Show could not be inserted into the database.')
    finally:
      db.session.close()
  if not valid:
    flash('An error occurred. Show form has an error in a field.')
  # on successful db insert, flash success

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
