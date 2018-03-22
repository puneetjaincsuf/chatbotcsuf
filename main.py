import logging
import settings

import models
from flask import jsonify, request
import base64
import json
from flask_cors import cross_origin
import api.services

app = api.app

models.db.init_app(app)
models.db.app = app

models.ma.init_app(app)
#models.ma.app = app;

app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

def _base64_decode(encoded_str):
    # Add paddings manually if necessary.
    num_missed_paddings = 4 - len(encoded_str) % 4
    if num_missed_paddings != 4:
        encoded_str += b'=' * num_missed_paddings
    return base64.b64decode(encoded_str).decode('utf-8')



def auth_info():
    """Retrieves the authenication information from Google Cloud Endpoints."""
    encoded_info = request.headers.get('X-Endpoint-API-UserInfo', None)

    if encoded_info:
        info_json = _base64_decode(encoded_info)
        user_info = json.loads(info_json)
    else:
        user_info = {'id': 'anonymous'}

    return jsonify(user_info)


@app.route('/auth/info/googlejwt', methods=['GET'])
def auth_info_google_jwt():
    """Auth info with Google signed JWT."""
    return auth_info()


@app.route('/auth/info/googleidtoken', methods=['GET'])
def auth_info_google_id_token():
    """Auth info with Google ID token."""
    return auth_info()


@app.route('/auth/info/firebase', methods=['GET'])
@cross_origin(send_wildcard=True)
def auth_info_firebase():
    """Auth info with Firebase auth."""
    return auth_info()



'''
def initialize_app(flask_app):
    configure_app(flask_app)
    db.init_app(flask_app)
'''

def main():
    #initialize_app(app)
    #db.init_app(app);
    app.run(host='127.0.0.1', port=8080, debug=True)
    #log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    #app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()

