from odp.ui.base.forms import BaseForm, DateStringField

import re
from flask import Flask, session
from wtforms.csrf.session import SessionCSRF
from wtforms import BooleanField, DateField, FloatField, Form, SelectField, SelectMultipleField, StringField, \
    TextAreaField, ValidationError
from wtforms.validators import optional, length, regexp


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
