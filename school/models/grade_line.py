# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class GradeLine(models.Model):
    """Defining grade line."""

    _name = "grade.line"
    _description = "Grades"
    _rec_name = "grade"

    from_mark = fields.Integer(
        "From Marks",
        required=True,
        help="The grade will starts from this marks.",
    )
    to_mark = fields.Integer(
        "To Marks", required=True, help="The grade will ends to this marks."
    )
    grade = fields.Char("Grade", required=True, help="Grade")
    sequence = fields.Integer("Sequence", help="Sequence order of the grade.")
    fail = fields.Boolean(
        "Fail",
        help="""If fail field is set to True,
it will allow you to set the grade as fail.""",
    )
    grade_id = fields.Many2one("grade.master", "Grade Ref.", help="Related grade")
    name = fields.Char("Name", help="Grade name")

    @api.constrains("from_mark", "to_mark")
    def check_marks(self):
        """Method to check overlapping of Marks"""
        for rec in self:
            if rec.to_mark < rec.from_mark:
                raise ValidationError(_("To Marks should be greater than From Marks!"))
            for line in self.search(
                [("grade_id", "=", rec.grade_id.id), ("id", "!=", rec.id)]
            ):
                if (
                    line.from_mark <= rec.from_mark <= line.to_mark
                    or line.from_mark <= rec.to_mark <= line.to_mark
                ):
                    raise ValidationError(
                        _("Error! You cannot define overlapping Marks!")
                    )
