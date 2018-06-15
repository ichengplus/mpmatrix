# coding=utf8

from flask import Flask, render_template, jsonify, Blueprint
from random import *
import os
import logging.config
from flask_cors import CORS
from flask_restplus import Resource, Api

from conf import settings
from api.blog.endpoints.posts import ns as blog_posts_namespace
from api.blog.endpoints.categories import ns as blog_categories_namespace
from api.restplus import api
from model import db, reset_database

# logging
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), './conf/logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

# app and api
app = Flask(__name__,
            static_folder = "../dist/static",
            template_folder = "../dist")

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(blog_posts_namespace)
    api.add_namespace(blog_categories_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)

@app.route('/init/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    reset_database()
    return jsonify(response)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == '__main__':
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)
