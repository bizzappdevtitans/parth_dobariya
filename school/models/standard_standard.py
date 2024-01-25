import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class StandardStandard(models.Model):
    """Defining Standard Information."""

    _name = "standard.standard"
    _description = "Standard Information"
    _order = "sequence"

    sequence = fields.Integer("Sequence", required=True, help="Sequence of the record")
    name = fields.Char("Name", required=True, help="Standard name")
    code = fields.Char("Code", required=True, help="Code of standard")
    description = fields.Text("Description", help="Description")

    @api.model
    def next_standard(self, sequence):
        """This method check sequence of standard"""
        stand_rec = self.search([("sequence", ">", sequence)], order="id", limit=1)
        return stand_rec and stand_rec.id or False
