from flask import Flask, Blueprint, request, session


def init_app(app: Flask):
    from . import home, surveys, vos_surveys, download_history

    app.register_blueprint(home.bp)
    app.register_blueprint(surveys.bp, url_prefix='/surveys')
    app.register_blueprint(vos_surveys.bp, url_prefix='/vos_surveys')
    app.register_blueprint(download_history.bp, url_prefix='/downloads')

    @app.context_processor
    def inject_globals():
        return {
            'marine_survey_types': [
                {'code': 1, 'name': 'Hydro'},
                {'code': 2, 'name': 'Currents'},
                {'code': 3, 'name': 'Weather'},
                {'code': 4, 'name': 'Waves'},
                {'code': 5, 'name': 'Echo-Sounding'},
                {'code': 6, 'name': 'UTR'},
            ]
        }
