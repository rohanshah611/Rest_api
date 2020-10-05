import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True
#sw
#return all tracks
@app.route('/resources/tracks/all', methods=['GET'])
def api_all_tracks():
    conn = sqlite3.connect('chinook.db')
    cur = conn.cursor()
    all_tracks = cur.execute('SELECT * FROM tracks;').fetchall()
    return jsonify(all_tracks)


#return all artists
@app.route('/resources/artists/all', methods=['GET'])
def api_all_artists():
    conn = sqlite3.connect('chinook.db')
    cur = conn.cursor()
    all_tracks = cur.execute('SELECT * FROM artists;').fetchall()
    return jsonify(all_tracks)


#get all tracks from a particular artists
@app.route('/resources/tracks/artists', methods=['GET'])
def api_filter_songs_based_on_artists():
    query_parameters = request.args
    artistid = query_parameters.get('artistid')
    query = "SELECT * FROM artists a join albums b on a.artistid=b.artistid join tracks c on b.albumid=c.albumid WHERE  "
    to_filter = []
    if artistid:
        query += ' a.artistid=? AND'
        to_filter.append(artistid)
    if not (artistid):
        return page_not_found(404)
    query = query[:-4] + ';'
    conn = sqlite3.connect('chinook.db')
    #conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()
    #print(results)
    return jsonify(results)


#returns all tracks from a particular genre
@app.route('/resources/tracks/genre', methods=['GET'])
def api_filter_songs_based_on_genres():
    query_parameters = request.args
    name = query_parameters.get('name')
    query = "SELECT * FROM genres a join tracks b on a.genreid=b.genreid WHERE  "
    to_filter = []
    if name:
        query += ' a.name=? AND'
        to_filter.append(name)
    if not (name):
        return page_not_found(404)
    query = query[:-4] + ';'
    conn = sqlite3.connect('chinook.db')
    #conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()
    #print(results)
    return jsonify(results)

#returns all gneres
@app.route('/resources/genres/all', methods=['GET'])
def api_all_genres():
    conn = sqlite3.connect('chinook.db')
    cur = conn.cursor()
    all_tracks = cur.execute('SELECT * FROM genres;').fetchall()
    return jsonify(all_tracks)


@app.route('/resources/tracks/details', methods=['GET'])
def api_track_details():
    query_parameters = request.args
    name = query_parameters.get('name')
    query = "SELECT * FROM genres a join tracks b on a.genreid=b.genreid join albums c on b.albumid=c.albumid join artists d on c.artistid=d.artistid WHERE  "
    to_filter = []
    if name:
        query += ' a.name=? AND'
        to_filter.append(name)
    if not (name):
        return page_not_found(404)
    query = query[:-4] + ';'
    conn = sqlite3.connect('chinook.db')
    #conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()
    #print(results)
    return jsonify(results)



#get all details for a particular track


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
app.run()
