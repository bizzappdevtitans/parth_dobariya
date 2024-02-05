# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _




class StudentFamilyContact(models.Model):
    """Defining a student emergency contact information"""

    _name = "student.family.contact"
    _description = "Student Family Contact"

    @api.depends("relation", "stu_name")
    def _compute_get_name(self):
        for rec in self:
            relative_name = rec.name
            if rec.stu_name:
                rec.relative_name = rec.stu_name.name
            rec.relative_name = relative_name

    family_contact_id = fields.Many2one(
        "student.student", "Student Ref.", help="Enter related student"
    )
    rel_name = fields.Selection(
        [
            ("exist", "Link to Existing Student"),
            ("new", "Create New Relative Name"),
        ],
        "Related Student",
        help="Select Name",
        required=True,
    )
    user_id = fields.Many2one(
        "res.users",
        "User ID",
        ondelete="cascade",
        help="Enter related user of the student",
    )
    stu_name = fields.Many2one(
        "student.student",
        "Existing Student",
        help="Select Student From Existing List",
    )
    name = fields.Char("Relative Name", help="Enter relative name")
    relation = fields.Many2one(
        "student.relation.master",
        "Relation",
        required=True,
        help="Select student relation with member",
    )
    phone = fields.Char("Phone", required=True, help="Enter family member contact")
    email = fields.Char("E-Mail", help="Enter student email")
    relative_name = fields.Char(
        compute="_compute_get_name",
        string="Name",
        help="Enter student family member name",
    )
