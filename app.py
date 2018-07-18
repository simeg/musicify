import logging
import os

from flask import \
    Flask, \
    abort, \
    jsonify, \
    make_response, \
    redirect, \
    render_template, \
    request, \
    send_from_directory

from src import spotify_auth, spotify_client, emotion_client, utils
from src.utils import exists, allowed_file_type

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

    cookie_token = request.cookies.get("spotify_token")
    if exists(cookie_token):
        logger.info("Token found")

        current_token = spotify_auth.cookie_to_dict(cookie_token)
        if spotify_auth.is_token_expired(current_token):
            logger.info("Token is expired - requesting new token")
            refresh_token = spotify_auth.refresh_token(current_token)
            refresh_token['refresh_token'] = current_token['refresh_token']
            current_token = refresh_token

        logger.info("Redirecting to /mix")
        response = make_response(redirect('/mix'))
        cookie = spotify_auth.json_to_cookie(current_token)
        logger.info("Setting token as cookie: %s" % cookie)
        response.set_cookie("spotify_token", cookie)

        return response
    else:
        logger.info("No token found - getting one")
        return redirect(spotify_auth.auth_url(), code=302)


@app.route('/callback', methods=['GET'])
def _callback():
    logger.info('/callback called')

    token = spotify_auth.request_new_token(request)

    response = make_response(redirect('/mix'))
    cookie = spotify_auth.json_to_cookie(token)
    logger.info("Setting token as cookie: %s" % cookie)
    response.set_cookie("spotify_token", cookie)

    return response


@app.route('/mix', methods=['GET'])
def _mix():
    logger.info('/mix called')
    if request.cookies.get("spotify_token") is None:
        logger.info("No auth cookie found - redirecting to /login")
        return redirect("/login", code=302)

    return make_response(render_template('mix.html'))


@app.route('/v1/tracks', methods=['POST'])
def _tracks():
    logger.info('/v1/tracks called')

    # TODO: Move validation downstream?
    if 'face_image' not in request.files:
        abort(400, 'No file with name \'face_image\' sent')  # Bad request
    else:
        image = request.files['face_image']
        if image and allowed_file_type(image.filename):
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
