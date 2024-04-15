from flask import Blueprint, abort, current_app, make_response, redirect, render_template, request, url_for
from odp.ui.base import cli
from sadco.const import SurveyType
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
        f'/survey/surveys/search',
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


@bp.route('/<survey_type>/<survey_id>')
@cli.view()
def survey_detail(survey_type, survey_id):
    survey = cli.get(f'/survey/{survey_type}/{survey_id}')
    return render_template(get_survey_type_template(survey['survey_type']), survey=survey)


def get_survey_type_template(survey_type) -> str:
    match survey_type:
        case SurveyType.HYDRO:
            return 'marine_survey_detail.html'
        case SurveyType.CURRENTS:
            return ''
        case SurveyType.WEATHER:
            return ''
        case SurveyType.WAVES:
            return ''
        case SurveyType.ECHOSOUNDING:
            return ''
        case SurveyType.UTR:
            return ''
        case SurveyType.VOS:
            return ''
        case SurveyType.UNKNOWN:
            return ''
