from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)

    from app.errors import bp as errors_bp
    from app.auth import bp as auth_bp, routes

    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    def root():
        return redirect(url_for("auth.index"))

    if not app.debug and not app.testing:
        if app.config["MAIL_SERVER"]:
            auth = None
            if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
                auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            secure = None
            if app.config["MAIL_USE_TLS"]:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost = (app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                fromaddr = "no-reply@" + app.config["MAIL_SERVER"],
                toaddrs = app.config["ADMINS"], subject = "Server Failure",
                credentials = auth, secure = secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    return app

app = create_app(Config)
from app import models