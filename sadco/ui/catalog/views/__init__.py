from flask import Flask, Blueprint, request, session


def init_app(app: Flask):
    from . import home, surveys, vos_surveys, download_audit

    app.register_blueprint(home.bp)
    app.register_blueprint(surveys.bp, url_prefix='/surveys')
    app.register_blueprint(vos_surveys.bp, url_prefix='/vos_surveys')
    app.register_blueprint(download_audit.bp, url_prefix='/downloads')




