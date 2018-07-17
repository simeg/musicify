import logging
import os

from flask import \
    Flask, \
    jsonify, \
    make_response, \
    request, \
    send_from_directory, \
    render_template, \
    abort

from src import spotify_auth, spotify_client, emotion_client, utils

app = Flask(__name__, static_folder='static')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_production = bool(os.environ.get('IS_PRODUCTION', default=False))


@app.route('/')
def _index():
    return render_template('index.html')


@app.route('/v1/tracks', methods=['POST'])
def _tracks():
    logger.info('/v1/tracks called')

    # TODO: Move validation downstream?
    if 'face_image' not in request.files:
        abort(400, 'No file with name \'face_image\' sent')  # Bad request
    else:
        image = request.files['face_image']
        if image and utils.allowed_file_type(image.filename):
            tracks = spotify_client.get_personalised_tracks(
                emotion_client.get_emotions(image.read()), limit=5)
            return jsonify({
                'tracks': tracks
            })
        else:
            abort(400, 'Image extension not allowed')  # Bad request


@app.route('/auth-callback', methods=['get'])
def _auth_callback():
    logger.info('/auth-callback called')
    return jsonify({
        'response': spotify_auth.request_token(request)
    })


@app.route('/v1/auth', methods=['get'])
def _auth():
    logger.info('/v1/auth called')
    return spotify_auth.auth_url()


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def _robots():
    return send_from_directory(app.static_folder, request.path[1:])


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(502)
def _handle_error(error):
    return make_response(jsonify({
        'error_msg': error.description,
        'error_code': int(error.code),
    }), error.code)


if __name__ == '__main__':
    # Flask server is only used during development
    if not is_production:
        app.run(debug=True, host='0.0.0.0', port=8000)
