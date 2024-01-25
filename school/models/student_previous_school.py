# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _




class StudentPreviousSchool(models.Model):
    """Defining a student previous school information"""

    _name = "student.previous.school"
    _description = "Student Previous School"

    previous_school_id = fields.Many2one(
        "student.student", "Student", help="Related student"
    )
    name = fields.Char("Name", required=True, help="Student previous school name")
    registration_no = fields.Char(
        "Registration No.", required=True, help="Student registration number"
    )
    admission_date = fields.Date("Admission Date", help="Student admission date")
    exit_date = fields.Date("Exit Date", help="Student previous school exit date")
    course_id = fields.Many2one(
        "standard.standard", "Course", required=True, help="Student gender"
    )
    add_sub = fields.One2many(
        "academic.subject", "add_sub_id", "Add Subjects", help="Student gender"
    )

    @api.constrains("admission_date", "exit_date")
    def check_date(self):
        new_dt = fields.Date.today()
        if (self.admission_date and self.admission_date >= new_dt) or (
            self.exit_date and self.exit_date >= new_dt
        ):
            raise ValidationError(
                _(
                    "Your admission date and exit date should be less than "
                    "current date!"
                )
            )
        if (self.admission_date and self.exit_date) and (
            self.admission_date > self.exit_date
        ):
            raise ValidationError(
                _("Admission date should be less than exit date in previous school!")
            )
