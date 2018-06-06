import logging
import os

from flask import Flask, jsonify, make_response, request, send_from_directory

from src import spotify_client, emotion_client

STATIC_FOLDER = 'src/resources'
app = Flask(__name__, static_folder=STATIC_FOLDER)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_production = bool(os.environ.get('IS_PRODUCTION', default=False))


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(502)
def _handle_error(error):
    return make_response(jsonify({
        'error_msg': error.description,
        'error_code': int(error.code),
    }), error.code)


@app.route('/v1/tracks', methods=['POST', 'GET'])
def _tracks():
    logger.info("/v1/tracks called")
    # image = request.files['TODO'] or None
    #
    face_emotions = emotion_client.get_emotions({})
    tracks = spotify_client.get_personalised_tracks(face_emotions, limit=2)
    #
    return jsonify({
        'tracks': tracks
    })


@app.route('/')
def _index():
    return jsonify({
        'author': 'Simon Egersand',
        'author_url': 'https://github.com/simeg',
        'base_url': 'https://github.com/simeg/moodify',
        'project_name': 'moodify',
        'project_url': 'https://github.com/simeg/moodify',
        'latest_version': 1,
    })


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def _robots():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == '__main__':
    # Flask server is only used during development
    if not is_production:
        # emotions = {
        #     'anger': 0.0,
        #     'contempt': 0.0,
        #     'disgust': 0.0,
        #     'fear': 0.0,
        #     'sadness': 0.0,
        #     'happiness': 0.196,
        #     'neutral': 0.0,
        #     'surprise': 0.803
        # }
        # tracks = spotify_client.get_personalised_tracks(emotions, 20)
        # print(tracks)
        app.run(debug=True, host='0.0.0.0', port=8000)
