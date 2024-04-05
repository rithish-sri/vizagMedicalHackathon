from flask import Flask
from flask import render_template
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    import db
    db.init_app(app)

    import auth
    app.register_blueprint(auth.bp)

    import dash
    app.register_blueprint(dash.bp)

    @app.route("/")
    def base():
        return render_template("base.html")

    
    return app




