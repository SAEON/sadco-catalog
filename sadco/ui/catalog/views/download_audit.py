from flask import Blueprint, render_template, request
from sadco.const import SADCOScope
from odp.ui.base import api

bp = Blueprint('download_audit', __name__, static_folder='../static')


@bp.route('/', methods=('GET',))
@api.view(SADCOScope.DOWNLOAD_READ)
def index():
    page = request.args.get('page', 1)
    downloads = api.get('/downloads/my_downloads', page=page)

    return render_template(
        'downloads.html',
        all_downloads_required_scope=SADCOScope.DOWNLOAD_ADMIN,
        downloads_type='my',
        result=downloads
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
    )
