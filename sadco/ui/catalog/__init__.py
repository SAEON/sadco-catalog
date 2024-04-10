from pathlib import Path

from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader

from sadco.config import sadco_config
from sadco.ui.catalog import views
from odp.ui import base


def create_app():
    """
    Flask application factory.
    """
    app = Flask(__name__)
    app.config.update(
        CI_CLIENT_ID=sadco_config.SADCO.CATALOG.CI_CLIENT_ID,
        CI_CLIENT_SECRET=sadco_config.SADCO.CATALOG.CI_CLIENT_SECRET,
        CI_CLIENT_SCOPE=[
            'SADCO'
        ],
        SECRET_KEY=sadco_config.SADCO.CATALOG.FLASK_SECRET,
    )

    base.init_app(app, client_api=True, template_dir=Path(__file__).parent / 'templates',
                  macro_dir=Path(__file__).parent / 'macros', api_url=sadco_config.SADCO.API_URL)

    views.init_app(app)

    return app
