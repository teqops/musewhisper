from flask import Flask
from src.config import Config


app = Flask(__name__)
app.config.from_object(Config)


def register_blueprint(app):
    from src.routes.general import general_blueprint
    from src.routes.api import api_blueprint
    app.register_blueprint(general_blueprint)
    app.register_blueprint(api_blueprint)


register_blueprint(app)
