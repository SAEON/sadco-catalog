from odp.ui.base.forms import BaseForm, DateStringField

from wtforms import BooleanField, FloatField, SelectField, StringField
from wtforms.validators import optional


class SearchForm(BaseForm):
    q = StringField(filters=[lambda s: s.strip() if s else s])
    n = FloatField()
    e = FloatField()
    s = FloatField()
    w = FloatField()
    survey_id = StringField(validators=[optional()], label='Survey ID')
    after = DateStringField(validators=[optional()], label='Start date')
    before = DateStringField(validators=[optional()], label='End date')
    exclusive_region = BooleanField(label='Exclusive region')
    exclusive_interval = BooleanField(label='Exclusive interval')


class HydroDownloadForm(BaseForm):
    data_type = SelectField(label='Data type')
