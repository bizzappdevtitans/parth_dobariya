# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class SubjectSyllabus(models.Model):
    """Defining a  syllabus"""

    _name = "subject.syllabus"
    _description = "Syllabus"
    _rec_name = "subject_id"

    standard_id = fields.Many2one(
        "school.standard", "Standard", help="Standard which had this subject"
    )
    subject_id = fields.Many2one("subject.subject", "Subject", help="Subject")
    syllabus_doc = fields.Binary(
        "Syllabus Doc", help="Attach syllabus related to Subject"
    )
