# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _




class StudentReminder(models.Model):
    """Defining student reminder."""

    _name = "student.reminder"
    _description = "Student Reminder"

    @api.model
    def check_user(self):
        """Method to get default value of logged in Student"""
        return self.env["student.student"].search([("user_id", "=", self._uid)]).id

    stu_id = fields.Many2one(
        "student.student",
        "Student Name",
        required=True,
        default=check_user,
        help="Relative student",
    )
    name = fields.Char("Title", help="Reminder name")
    date = fields.Date("Date", help="Reminder date")
    description = fields.Text("Description", help="Description of the reminder")
    color = fields.Integer("Color Index", default=0, help="Color index")

    @api.constrains("date")
    def check_date(self):
        """Method to check constraint of due date and assign date"""
        if self.date < fields.Date.today():
            raise ValidationError(
                _("Reminder date of must be greater or equal current date !")
            )
