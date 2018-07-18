import logging
import os

from flask import \
    Flask, \
    jsonify, \
    make_response, \
    request, \
    send_from_directory, \
    render_template, \
    abort, redirect

from src import spotify_auth, spotify_client, emotion_client, utils

app = Flask(__name__, static_folder='static')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IS_PRODUCTION = bool(os.environ.get('IS_PRODUCTION', default=False))


@app.route('/', methods=['GET'])
def _index():
    logger.info('/ called')
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def _login():
    logger.info('/login called')

    token = spotify_auth.get_token()
    if token is not None:
        logger.info("Token found")

        if spotify_auth.is_token_expired(token):
            logger.info("Token is expired - requesting new token")
            refresh_token = spotify_auth.refresh_token(token)
            refresh_token['refresh_token'] = token['refresh_token']
            spotify_auth.cache_token(refresh_token)

        return redirect('/mix')
    else:
        logger.info("No token found - getting one")
        return redirect(spotify_auth.auth_url(), code=302)


@app.route('/callback', methods=['GET'])
def _callback():
    logger.info('/callback called')
    spotify_auth.request_token(request)
    return redirect('/mix')


@app.route('/v1/auth', methods=['GET'])
def _auth():
    logger.info('/v1/auth called')
    return spotify_auth.auth_url()


@app.route('/mix', methods=['GET'])
def _mix():
    logger.info('/mix called')
    return render_template('mix.html')


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
    if not IS_PRODUCTION:
        app.run(debug=True, host='0.0.0.0', port=8000)
