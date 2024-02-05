import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class StandardDivision(models.Model):
    """Defining a division(A, B, C) related to standard"""

    _name = "standard.division"
    _description = "Standard Division"
    _order = "sequence"

    sequence = fields.Integer("Sequence", required=True, help="Sequence of the record")
    name = fields.Char("Name", required=True, help="Division of the standard")
    code = fields.Char("Code", required=True, help="Standard code")
    description = fields.Text("Description", help="Description")
