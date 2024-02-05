# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class SchoolSchool(models.Model):
    """Defining School Information"""

    _name = "school.school"
    _description = "School Information"
    _rec_name = "com_name"

    @api.constrains("code")
    def _check_code(self):
        for record in self:
            if self.env["school.school"].search(
                [("code", "=", record.code), ("id", "!=", record.id)]
            ):
                raise ValidationError(_("School Code must be Unique"))

    @api.model
    def _lang_get(self):
        """Method to get language"""
        languages = self.env["res.lang"].search([])
        return [(language.code, language.name) for language in languages]

    company_id = fields.Many2one(
        "res.company",
        "Company",
        ondelete="cascade",
        required=True,
        delegate=True,
        help="Company_id of the school",
    )
    com_name = fields.Char(
        "School Name",
        related="company_id.name",
        store=True,
        help="School name",
    )
    code = fields.Char("Code", required=True, help="School code")
    standards = fields.One2many(
        "school.standard", "school_id", "Standards", help="School standard"
    )
    lang = fields.Selection(
        _lang_get,
        "Language",
        help="""If the selected language is loaded in the
                                system, all documents related to this partner
                                will be printed in this language.
                                If not, it will be English.""",
    )
    required_age = fields.Integer(
        "Student Admission Age Required",
        default=6,
        help="""Minimum required age for
                                  student admission""",
    )

    @api.model
    def create(self, vals):
        """Inherited create method to assign company_id to school"""
        res = super(SchoolSchool, self).create(vals)
        main_company = self.env.ref("base.main_company")
        res.company_id.parent_id = main_company.id
        return res
