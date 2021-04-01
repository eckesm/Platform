from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_redis import FlaskRedis
# from flask_assets import Environment
from flask_debugtoolbar import DebugToolbarExtension
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail, Message
# from .assets import compile_static_assets
from .models import db, User, Group, Membership, Post
# from .secret import MAIL_USERNAME, MAIL_PASSWORD
from .admin import AdminView

# db = SQLAlchemy()
# r = FlaskRedis()


def create_app():

    app = Flask(__name__, instance_relative_config=False)
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    # assets = Environment()

    # Initialize Plugins
    db.init_app(app)
    # r.init_app(app)
    # assets.init_app(app)

    with app.app_context():

        # Import parts of our application
        from .api.routes import api_bp
        from .auth.routes import auth_bp
        from .groups.routes import groups_bp
        from .home.routes import home_bp
        from .posts.routes import posts_bp
        from .users.routes import users_bp
        from .eurovision.routes import eurovision_bp

        debug = DebugToolbarExtension(app)

        admin = Admin(app, name='platform', template_mode='bootstrap3', index_view=AdminView(User,db.session,url='/admin', endpoint='admin'))
        admin.add_view(ModelView(User, db.session))
        admin.add_view(ModelView(Group, db.session))
        admin.add_view(ModelView(Membership, db.session))
        admin.add_view(ModelView(Post, db.session))

        app.register_blueprint(api_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(groups_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(posts_bp)
        app.register_blueprint(users_bp)
        app.register_blueprint(eurovision_bp)

        # Compile static assets
        # compile_static_assets(assets)

        return app
