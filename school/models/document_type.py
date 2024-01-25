import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _




class DocumentType(models.Model):
    """Defining a Document Type(SSC,Leaving)"""

    _name = "document.type"
    _description = "Document Type"
    _rec_name = "doc_type"
    _order = "seq_no"

    seq_no = fields.Char(
        "Sequence",
        readonly=True,
        default=lambda self: _("New"),
        help="Sequence of the document",
    )
    doc_type = fields.Char("Document Type", required=True, help="Document type")

    @api.model
    def create(self, vals):
        if vals.get("seq_no", _("New")) == _("New"):
            vals["seq_no"] = self.env["ir.sequence"].next_by_code("document.type") or _(
                "New"
            )
        return super(DocumentType, self).create(vals)
