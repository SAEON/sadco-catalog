from flask import Blueprint, abort, current_app, make_response, redirect, render_template, request, url_for
from odp.ui.base import cli
from sadco.ui.catalog.forms import SearchForm

bp = Blueprint('surveys', __name__,  static_folder='../static')

@bp.route('/')
@cli.view()
def index():
    survey_id = request.args.get('survey_id')
    north_bound = request.args.get('n')
    east_bound = request.args.get('e')
    south_bound = request.args.get('s')
    west_bound = request.args.get('w')
    start_date = request.args.get('after')
    end_date = request.args.get('before')
    exclusive_region = request.args.get('exclusive_region')
    exclusive_interval = request.args.get('exclusive_interval')
    sampling_device_code = request.args.get('sampling_device_code')
    page = request.args.get('page', 1)

    result = cli.get(
        f'/marine/surveys/search',
        survey_id=survey_id,
        north_bound=north_bound,
        east_bound=east_bound,
        south_bound=south_bound,
        west_bound=west_bound,
        start_date=start_date,
        end_date=end_date,
        exclusive_region=exclusive_region,
        exclusive_interval=exclusive_interval,
        sampling_device_code=sampling_device_code,
        page=page
    )

    return render_template(
        'survey_index.html',
        form=SearchForm(request.args),
        result=result,
    )


@bp.route('/search', methods=('POST',))
def search():
    form = SearchForm(request.form)
    query = form.data
    query.pop('csrf_token')
    if not query['exclusive_region']:
        query.pop('exclusive_region')
    if not query['exclusive_interval']:
        query.pop('exclusive_interval')

    return redirect(url_for('.index', **query))


@bp.route('/<id>')
@cli.view()
def survey_detail(id):
    survey = cli.get(f'/marine/surveys/{id}')
    return render_template('survey_detail.html', survey=survey)
