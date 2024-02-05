# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class StudentDocument(models.Model):
    """Defining Student document."""

    _name = "student.document"
    _description = "Student Document"
    _rec_name = "doc_type"

    doc_id = fields.Many2one(
        "student.student", "Student", help="Student of the following doc"
    )
    file_no = fields.Char(
        "File No",
        readonly="1",
        default=lambda obj: obj.env["ir.sequence"].next_by_code("student.document"),
        help="File no of the document",
    )
    submited_date = fields.Date("Submitted Date", help="Document submitted date")
    doc_type = fields.Many2one(
        "document.type", "Document Type", required=True, help="Document type"
    )
    file_name = fields.Char("File Name", help="File name")
    return_date = fields.Date("Return Date", help="Document return date")
    new_datas = fields.Binary("Attachments", help="Attachments of the document")
