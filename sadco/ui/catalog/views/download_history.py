import json
from pathlib import Path

from flask import Blueprint, render_template, request

from odp.ui.base import api
from sadco.const import SADCOScope, SurveyType
from .surveys import download_marine_data
from .vos_surveys import download_vos_data

bp = Blueprint('download_history', __name__, static_folder=Path(__file__).parent.parent / 'static',)


@bp.route('/', methods=('GET',))
@api.view(SADCOScope.DOWNLOAD_READ)
def index():
    page = request.args.get('page', 1)
    downloads = api.get('/downloads/my_downloads', page=page)

    return render_template(
        'downloads.html',
        all_downloads_required_scope=SADCOScope.DOWNLOAD_ADMIN,
        downloads_type='my',
        result=downloads,
        json=json
    )


@bp.route('/all_downloads', methods=('GET',))
@api.view(SADCOScope.DOWNLOAD_ADMIN)
def all_downloads():
    page = request.args.get('page', 1)
    downloads = api.get('/downloads/all_downloads', page=page)

    return render_template(
        'downloads.html',
        all_downloads_required_scope=SADCOScope.DOWNLOAD_ADMIN,
        downloads_type='all',
        result=downloads,
        json=json
    )


@bp.route('/re_download', methods=('GET',))
@api.view(SADCOScope.DOWNLOAD_READ)
def re_download():
    data = request.args.get('data')
    download_history_info = json.loads(data)
    survey_type = download_history_info['survey_type']
    download_parameters = download_history_info['parameters']

    match survey_type:
        case SurveyType.VOS:
            return download_vos_data(download_parameters)
        case _:
            survey_id = download_parameters['survey_id']
            data_type = download_parameters['data_type']
            return download_marine_data(survey_type, data_type, survey_id)

