import datetime
import logging
import os
from pathlib import Path

from flask import Flask
from app.engine.exceptions import exception_handler


# Flask quickstart:
# https://flask.palletsprojects.com/en/2.2.x/quickstart/
# Flask factory pattern:
# https://flask.palletsprojects.com/en/2.2.x/tutorial/factory/
def create_app():
    # Create and configure the app
    app = Flask(__name__)

    # Load config from file config.py
    app.config.from_pyfile("config.py")

    # Collect nice logs for debugging
    Path(os.path.join(app.root_path, app.config['LOG_DIR'])).mkdir(exist_ok=True)
    Path(os.path.join(app.root_path, app.config['DEBUG_LOG'])).touch(exist_ok=True)
    Path(os.path.join(app.root_path, app.config['ERROR_LOG'])).touch(exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(app.root_path, app.config['DEBUG_LOG']),
        level=logging.DEBUG,
        format=f'[%(asctime)s][%(levelname)s][%(name)s][%(threadName)s] %(message)s'
    )

    # Ensure the instance folder exists - nothing interesting
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_error_handler(Exception, exception_handler)

    @app.errorhandler(404)
    @app.errorhandler(405)
    def _handle_api_error(ex):
        return exception_handler(ex)

    # Register blueprints (views)
    # https://flask.palletsprojects.com/en/2.2.x/blueprints/
    from app.views.main import bp as bp_main
    app.register_blueprint(bp_main)


    # Import and register blueprints here

    return app
