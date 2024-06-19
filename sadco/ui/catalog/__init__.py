from pathlib import Path

from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader

from sadco.config import sadco_config
from sadco.const import SADCOScope
from odp.const import ODPScope
from sadco.ui.catalog import views
from odp.const.hydra import HydraScope
from odp.ui import base


def create_app():
    """
    Flask application factory.
    """
    app = Flask(__name__)
    app.config.update(
        UI_CLIENT_ID=sadco_config.SADCO.CATALOG.UI_CLIENT_ID,
        UI_CLIENT_SECRET=sadco_config.SADCO.CATALOG.UI_CLIENT_SECRET,
        UI_CLIENT_SCOPE=[
            HydraScope.OPENID,
            HydraScope.OFFLINE_ACCESS,
            SADCOScope.HYDRO_DOWNLOAD,
            SADCOScope.CURRENTS_DOWNLOAD,
            ODPScope.TOKEN_READ
        ],
        CI_CLIENT_ID=sadco_config.SADCO.CATALOG.CI_CLIENT_ID,
        CI_CLIENT_SECRET=sadco_config.SADCO.CATALOG.CI_CLIENT_SECRET,
        CI_CLIENT_SCOPE=[
            SADCOScope.SURVEYS_READ,
            SADCOScope.HYDRO_READ,
            SADCOScope.CURRENTS_READ
        ],
        SECRET_KEY=sadco_config.SADCO.CATALOG.FLASK_SECRET,
        CATALOG_TERMS_OF_USE='''
                These data are made available with the express understanding that any such use
                will properly acknowledge the originator(s) and publisher and cite the accession
                numbers and/or associated Digital Object Identifiers. Anyone wishing to use these
                data should properly cite and attribute the data providers listed as authors in
                the metadata provided with each dataset. It is expected that all the conditions
                of the data license will be strictly honoured. Use of any material herein should
                be properly cited using the dataset’s persistent identifiers such as accession
                numbers and DOIs.
            ''',
    )

    base.init_app(app, user_api=True, client_api=True, template_dir=Path(__file__).parent / 'templates',
                  macro_dir=Path(__file__).parent / 'macros', api_url=sadco_config.SADCO.API_URL)

    views.init_app(app)

    return app
