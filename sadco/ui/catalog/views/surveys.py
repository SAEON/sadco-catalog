from flask import Blueprint, send_file, redirect, render_template, request, url_for
from odp.ui.base import cli
from io import BytesIO
import zipfile
from sadco.const import SurveyType
from odp.ui.base.forms import BaseForm
from sadco.ui.catalog.forms import SearchForm, HydroDownloadForm
from sadco.const import DataType

bp = Blueprint('surveys', __name__, static_folder='../static')


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
    survey_type_code = request.args.get('survey_type_code')
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
        survey_type_code=survey_type_code,
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

    form = get_survey_type_form(survey, survey_type)

    return render_template(
        get_survey_type_template(survey_type),
        form=form,
        survey=survey
    )


@bp.route('/download/<survey_type>/<survey_id>', methods=('POST',))
def download(survey_type, survey_id):
    form = HydroDownloadForm(request.form)
    data_type = form.data['data_type']

    survey_data = cli.get_bytes(
        f'/survey/download/{survey_type}/{survey_id}',
        data_type=data_type
    )

    file_name = f'survey_{survey_id}_{data_type}.zip'

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr(file_name, survey_data)

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=file_name
    )


def get_survey_type_template(survey_type) -> str:
    """Get a template specific to a survey type"""
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


def get_survey_type_form(survey, survey_type) -> BaseForm:
    """Return a form specific to the survey type."""
    match survey_type:
        case SurveyType.HYDRO:
            return get_hydro_download_form(survey)
        case _:
            return BaseForm()


def get_hydro_download_form(survey) -> HydroDownloadForm:
    """Set the 'hydro form' select choices based on the surveys data types and return the form"""
    hydro_download_form = HydroDownloadForm(request.args)

    data_type_choices = []

    has_water_chemistry_and_nutrients = False

    for data_type, data_type_detail in survey['data_types'].items():

        if data_type_detail is None:
            continue
        data_type_choices.append((data_type, data_type.title().replace('_', ' ')))

        if not has_water_chemistry_and_nutrients and data_type_detail.get(
                DataType.WATERCHEMISTRY) and data_type_detail.get(DataType.WATERNUTRIENTS):
            has_water_chemistry_and_nutrients = True

        for sub_data_type, sub_data_type_detail in data_type_detail.items():

            if sub_data_type != 'record_count' and sub_data_type_detail is not None:
                data_type_choices.append((sub_data_type, sub_data_type.title().replace('_', ' ')))

        if has_water_chemistry_and_nutrients:
            has_water_chemistry_and_nutrients = False
            data_type_choices.append(
                (DataType.WATERNUTRIENTSANDCHEMISTRY.value, DataType.WATERNUTRIENTSANDCHEMISTRY.title().replace('_', ' ')))

    hydro_download_form.data_type.choices = data_type_choices

    return hydro_download_form
