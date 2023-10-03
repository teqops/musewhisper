import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DEVELOPMENT = os.environ['DEVELOPMENT']
    DEBUG = os.environ['DEBUG']
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

    OPENAI_KEY = os.environ['OPENAI_KEY']
    WHOAPI_KEY = os.environ['WHOAPI_KEY']
