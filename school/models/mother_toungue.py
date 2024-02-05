# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class MotherTongue(models.Model):
    """Defining mother tongue."""

    _name = "mother.toungue"
    _description = "Mother Toungue"

    name = fields.Char("Mother Tongue", help="Language name")
