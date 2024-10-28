from flask import Blueprint, redirect, render_template, request, url_for
from odp.ui.base import cli, api
from sadco.const import SurveyType
from odp.ui.base.forms import BaseForm
from sadco.ui.catalog.forms import SearchForm, HydroDownloadForm
from sadco.ui.catalog.lib import download_zipped_file
from sadco.const import DataType, SADCOScope

bp = Blueprint('surveys', __name__, static_folder='../static')


@bp.route('/')
@cli.view()
@api.user()
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
    survey_type_code = request.args.get('survey_type_code')
    institute_code = request.args.get('institute_code')
    page = request.args.get('page', 1)

    result = cli.get(
        '/survey/surveys/search',
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
        survey_type_code=survey_type_code,
        institute_code=institute_code,
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
@api.user()
def survey_detail(survey_type, survey_id):
    survey = cli.get(f'/survey/{survey_type}/{survey_id}')

    return render_template(
        get_survey_type_template(survey_type),
        form=get_survey_type_form(survey, survey_type),
        survey=survey,
        survey_type=survey_type
    )


@bp.route(f'/download/{SurveyType.HYDRO.value}/<survey_id>', methods=('POST',))
@api.view(SADCOScope.HYDRO_DOWNLOAD)
def hydro_download(survey_id):
    return download(SurveyType.HYDRO.value, survey_id)


@bp.route(f'/download/{SurveyType.CURRENTS.value}/<survey_id>', methods=('POST',))
@api.view(SADCOScope.CURRENTS_DOWNLOAD)
def currents_download(survey_id):
    return download(SurveyType.CURRENTS.value, survey_id)


@bp.route(f'/download/{SurveyType.WEATHER.value}/<survey_id>', methods=('POST',))
@api.view(SADCOScope.WEATHER_DOWNLOAD)
def weather_download(survey_id):
    return download(SurveyType.WEATHER.value, survey_id)


@bp.route(f'/download/{SurveyType.WAVES.value}/<survey_id>', methods=('POST',))
@api.view(SADCOScope.WAVES_DOWNLOAD)
def waves_download(survey_id):
    return download(SurveyType.WAVES.value, survey_id)


@bp.route(f'/download/{SurveyType.UTR.value}/<survey_id>', methods=('POST',))
@api.view(SADCOScope.UTR_DOWNLOAD)
def utr_download(survey_id):
    return download(SurveyType.UTR.value, survey_id)


def download(survey_type, survey_id):
    data_type = get_download_data_type(survey_type)

    survey_data = api.get_bytes(
        f'/survey/download/{survey_type}/{survey_id}',
        data_type=data_type
    )

    file_name = f'survey_{survey_id}_{data_type}.zip'

    return download_zipped_file(file_name, survey_data)


def get_download_data_type(survey_type) -> str:
    match survey_type:
        case SurveyType.HYDRO:
            form = HydroDownloadForm(request.form)
            return form.data['data_type']
        case _:
            return survey_type


def get_survey_type_template(survey_type) -> str:
    """
    Get a template specific to a survey type
    """
    match survey_type:
        case SurveyType.HYDRO:
            return 'hydro_survey_detail.html'
        case SurveyType.CURRENTS | SurveyType.UTR:
            return 'mooring_survey_detail.html'
        case SurveyType.WEATHER | SurveyType.WAVES:
            return 'survey_periods_detail.html'
        case SurveyType.ECHOSOUNDING | SurveyType.UNKNOWN:
            return 'survey_detail.html'
        case SurveyType.VOS:
            return ''


def get_survey_type_form(survey, survey_type) -> BaseForm:
    """
    Return a form specific to the survey type.
    """
    match survey_type:
        case SurveyType.HYDRO:
            return get_hydro_download_form(survey)
        case _:
            return BaseForm()


def get_hydro_download_form(survey) -> HydroDownloadForm:
    """
    Set the 'hydro form' select choices based on the surveys data types and return the form
    """
    hydro_download_form = HydroDownloadForm(request.args)

    data_type_choices = []

    has_water_chemistry_and_nutrients = False

    for data_type, data_type_detail in survey['data_types'].items():

        if data_type_detail is None:
            continue

        data_type_choices.append((data_type, data_type.title().replace('_', ' ')))

        for sub_data_type, sub_data_type_detail in data_type_detail.items():

            if sub_data_type != 'record_count' and sub_data_type_detail is not None:
                data_type_choices.append((sub_data_type, sub_data_type.title().replace('_', ' ')))

        # Appears within loop so that water and chemistry option shows in the right order
        if not has_water_chemistry_and_nutrients and data_type_detail.get(
                DataType.WATERCHEMISTRY) and data_type_detail.get(DataType.WATERNUTRIENTS):
            has_water_chemistry_and_nutrients = True
            data_type_choices.append(
                (DataType.WATERNUTRIENTSANDCHEMISTRY.value,
                 DataType.WATERNUTRIENTSANDCHEMISTRY.title().replace('_', ' ')))

    hydro_download_form.data_type.choices = data_type_choices

    return hydro_download_form
