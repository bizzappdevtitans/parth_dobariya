import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class StudentCast(models.Model):
    """Defining student cast."""

    _name = "student.cast"
    _description = "Student Cast"

    name = fields.Char("Name", required=True, help="Student cast")
