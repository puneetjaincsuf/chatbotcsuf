import os

# Flask settings
FLASK_SERVER_HOST = '127.0.0.1:8080'
FLASK_SERVER_PORT = '8080'
FLASK_DEBUG = False  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']