# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class StudentAward(models.Model):
    """Defining student award."""

    _name = "student.award"
    _description = "Student Awards"

    award_list_id = fields.Many2one(
        "student.student",
        "Student",
        help="Students who about to get the award",
    )
    name = fields.Char("Award Name", help="Award name")
    description = fields.Char("Description", help="Description")
