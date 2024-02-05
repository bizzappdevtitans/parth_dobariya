import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _

class SubjectElective(models.Model):
    """Defining Subject Elective"""

    _name = "subject.elective"
    _description = "Elective Subject"

    name = fields.Char("Name", help="Elective subject name")
    subject_ids = fields.One2many(
        "subject.subject",
        "elective_id",
        "Elective Subjects",
        help="Subjects of the respective elective subject",
    )
