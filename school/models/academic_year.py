# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class AcademicYear(models.Model):
    """Defines an academic year."""

    _name = "academic.year"
    _description = "Academic Year"
    _order = "sequence"

    sequence = fields.Integer(
        "Sequence",
        required=True,
        help="Sequence order you want to see this year.",
    )
    name = fields.Char("Name", required=True, help="Name of academic year")
    code = fields.Char("Code", required=True, help="Code of academic year")
    date_start = fields.Date(
        "Start Date", required=True, help="Starting date of academic year"
    )
    date_stop = fields.Date("End Date", required=True, help="Ending of academic year")
    month_ids = fields.One2many(
        "academic.month", "year_id", "Months", help="Related Academic months"
    )
    grade_id = fields.Many2one("grade.master", "Grade", help="Grade")
    current = fields.Boolean("Current", help="Set Active Current Year")
    description = fields.Text("Description", help="Description")

    @api.model
    def next_year(self, sequence):
        """This method assign sequence to years"""
        year_rec = self.search([("sequence", ">", sequence)], order="id", limit=1)
        if year_rec:
            return year_rec.id or False


    # ORM name_get method 
    def name_get(self):
        """Method to display name and code"""
        return [(rec.id, " [" + rec.code + "]" + rec.name) for rec in self]

    def generate_academicmonth(self):
        """Generate academic months."""
        interval = 1
        month_obj = self.env["academic.month"]
        for rec in self:
            start_date = rec.date_start
            while start_date < rec.date_stop:
                end_date = start_date + relativedelta(months=interval, days=-1)
                if end_date > rec.date_stop:
                    end_date = rec.date_stop
                month_obj.create(
                    {
                        "name": start_date.strftime("%B"),
                        "code": start_date.strftime("%m/%Y"),
                        "date_start": start_date,
                        "date_stop": end_date,
                        "year_id": rec.id,
                    }
                )
                start_date = start_date + relativedelta(months=interval)

    @api.constrains("date_start", "date_stop")
    def _check_academic_year(self):
        """Method to check start date should be greater than end date
        also check that dates are not overlapped with existing academic
        year"""
        new_start_date = self.date_start
        new_stop_date = self.date_stop
        delta = new_stop_date - new_start_date
        if delta.days > 365 and not calendar.isleap(new_start_date.year):
            raise ValidationError(_("The duration of the academic year is invalid."))
        if self.date_stop and self.date_start and self.date_stop < self.date_start:
            raise ValidationError(
                _(
                    "The start date of the academic year should be less than "
                    "end date."
                )
            )
        for old_ac in self.search([("id", "not in", self.ids)]):
            # Check start date should be less than stop date
            if (
                old_ac.date_start <= self.date_start <= old_ac.date_stop
                or old_ac.date_start <= self.date_stop <= old_ac.date_stop
            ):
                raise ValidationError(
                    _("Error! You cannot define overlapping academic years.")
                )

    @api.constrains("current")
    def check_current_year(self):
        """Constraint on active current year"""
        current_year_rec = self.search_count([("current", "=", True)])
        if current_year_rec >= 2:
            raise ValidationError(_("Error! You cannot set two current year active!"))
