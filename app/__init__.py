from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager, current_user
from config import config
from flask_debugtoolbar import DebugToolbarExtension

from flask_restful import Api

bootstrap = Bootstrap()
db = MongoEngine()
login_manager = LoginManager()
api = Api()



def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config[config_name])
    app.config['MONGODB_SETTINGS'] = {
        'db': config[config_name].MONGO_DATABASE_NAME,
        'host': config[config_name].MONGO_DATABASE_SERVER,
        'port': config[config_name].MONGO_DATABASE_PORT,
        'username': 'longhk',
        'password': 'abc@123#@!'

    }

    config[config_name].init_app(app)
    bootstrap.init_app(app)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    app.session_interface = MongoEngineSessionInterface(db)

    db.init_app(app)


    # Specify the debug panels you want
    app.config['DEBUG_TB_PANELS'] = [
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        # Add the MongoDB panel
        #'flask.ext.mongoengine.panels.MongoDebugPanel',
    ]
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    toolbar = DebugToolbarExtension(app)

    ############### begin blueprint ############################
    from app.controllers.auth import auth as auth_blueprint
    from app.controllers.home import home as home_blueprint
    from app.controllers.project import project as project_blueprint
    from app.controllers.source import source as source_blueprint
    #from app.controllers.service import service as service_blueprint
    app.register_blueprint(home_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(project_blueprint, url_prefix='/project')
    app.register_blueprint(source_blueprint, url_prefix='/source')

    ############### end blueprint   ################################

    ################# begin api ####################################
    from api.controllers.project import API_PROJECT, API_LIST_PROJECT, API_LIST_PROJECT_WITH_SERVERIP
    api.add_resource(API_LIST_PROJECT, '/api/v.1/projects')
    api.add_resource(API_PROJECT, '/api/v.1/projects/<string:project_id>')
    api.add_resource(API_LIST_PROJECT_WITH_SERVERIP, '/api/v.1/projects/server/<string:server_ip>')


    from api.controllers.source import API_SOURCE, API_LIST_SOURCE, API_SOURCE_CONFIG, API_SOURCE_BY_SERVER
    api.add_resource(API_LIST_SOURCE, '/api/v.1/sources')
    api.add_resource(API_SOURCE, '/api/v.1/sources/<string:source_id>')
    api.add_resource(API_SOURCE_BY_SERVER, '/api/v.1/sources/server/<string:server_ip>')
    api.add_resource(API_SOURCE_CONFIG, '/api/v.1/sources/config/<string:key_config>/<string:s_id>')

    ################################################################
    api.init_app(app)


    return app


