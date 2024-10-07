from flask import Blueprint, render_template
from sadco.const import SADCOScope
from odp.ui.base import api

bp = Blueprint('download_audit', __name__, static_folder='../static')


@bp.route('/', methods=('GET',))
@api.view(SADCOScope.DOWNLOAD_READ)
def index():
    downloads = api.get('/downloads/my_downloads')

    return render_template(
        'downloads.html',
        downloads_type='my',
        result=downloads
    )


@bp.route('/all_downloads', methods=('GET',))
@api.view(SADCOScope.DOWNLOAD_ADMIN)
def all_downloads():
    downloads = api.get('/downloads/all_downloads')

    return render_template(
        'downloads.html',
        downloads_type='all',
        result=downloads,
    )
