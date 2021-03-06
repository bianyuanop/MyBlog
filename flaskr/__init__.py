import os
import re
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
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

    

    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import upload
    app.register_blueprint(upload.bp)
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    from . import me
    app.register_blueprint(me.bp)
    from . import admin
    app.register_blueprint(admin.bp)
    

    @app.template_filter('cut')
    def cut(value):
        value = value.replace("*", '')
        value = value.replace("#", '')
        value = re.sub("!{1}\[{1}\]{1}\({1}.*\){1}", "图片", value)
        value = re.sub("(\[.*\]:*)+", '', value)
        return value
    
    return app
