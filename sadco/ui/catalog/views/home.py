from pathlib import Path
import os, json
from flask import Blueprint, render_template, send_file, abort

from sadco.ui.catalog.forms import SearchForm

bp = Blueprint(
    'home', __name__,
    static_folder=Path(__file__).parent.parent / 'static',
    static_url_path='/static/mims',
)


@bp.route('/')
def index():
    return render_template(
        'home.html',
        search_form=SearchForm(),
    )


@bp.route('/history')
def history():
    return render_template(
        'history.html',
    )


@bp.route('/data_types')
def data_types():
    return render_template(
        'data_types.html',
    )


@bp.route('/users_guide')
def users_guide():
    return render_template(
        'users_guide.html',
    )


@bp.route('/newsletters')
def newsletters():
    newsletters_json_file_path = os.path.join(bp.static_folder, 'newsletters/newsletters.json')

    with open(newsletters_json_file_path, 'r') as file:
        newsletters_list = json.load(file)

    return render_template(
        'newsletters.html',
        newsletters_list=newsletters_list
    )


@bp.route('/newsletter_download/<year>/<file_name>')
def newsletter_download(year, file_name):
    file_path = os.path.join(bp.static_folder, 'newsletters', year, file_name)

    if not os.path.isfile(file_path):
        abort(404)

    return send_file(file_path, mimetype='application/zip')
