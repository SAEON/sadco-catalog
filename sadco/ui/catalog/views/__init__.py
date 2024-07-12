from flask import Flask, Blueprint, request, session
from pathlib import Path


def init_app(app: Flask):
    from . import home, surveys

    app.register_blueprint(home.bp)
    app.register_blueprint(surveys.bp, url_prefix='/surveys')



