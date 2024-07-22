from flask import Blueprint, redirect, render_template, request, url_for, session
from odp.ui.base import cli, api
from sadco.ui.catalog.forms import SearchForm
from sadco.ui.catalog.lib import download_zipped_file

bp = Blueprint('vos_surveys', __name__, static_folder='../static')


@bp.route('/')
@cli.view()
@api.user()
def index():
    search_bounds = get_search_bounds()

    session['search_bounds'] = search_bounds

    result = cli.get(
        '/vos_survey/vos_surveys/search',
        **search_bounds
    )

    return render_template(
        'vos_survey_index.html',
        form=SearchForm(request.args),
        result=result,
    )


@bp.route('/search', methods=('POST',))
def search():
    query = get_search_query()

    return redirect(url_for('.index', **query))


@bp.route('/vos_download')
def vos_download():
    search_bounds = session['search_bounds']

    vos_survey_data = api.get_bytes(
        '/vos_survey/download',
        **search_bounds
    )

    filename = 'vos_surveys.zip'

    return download_zipped_file(filename, vos_survey_data)


@bp.route('/download', methods=('POST',))
def download():
    query = get_search_query()

    return redirect(url_for('.vos_download', **query))


def get_search_bounds() -> dict:
    return dict(
        north_bound=request.args.get('n'),
        east_bound=request.args.get('e'),
        south_bound=request.args.get('s'),
        west_bound=request.args.get('w'),
        start_date=request.args.get('after'),
        end_date=request.args.get('before'),
        exclusive_region=request.args.get('exclusive_region'),
        exclusive_interval=request.args.get('exclusive_interval'),
        page=request.args.get('page', 1)
    )


def get_search_query():
    form = SearchForm(request.form)
    query = form.data
    query.pop('csrf_token')
    if not query['exclusive_region']:
        query.pop('exclusive_region')
    if not query['exclusive_interval']:
        query.pop('exclusive_interval')

    return query
