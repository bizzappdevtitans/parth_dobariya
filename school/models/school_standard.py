# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class SchoolStandard(models.Model):
    """Defining a standard related to school."""

    _name = "school.standard"
    _description = "School Standards"
    _rec_name = "standard_id"

    @api.depends("standard_id", "school_id", "division_id", "medium_id", "school_id")
    def _compute_student(self):
        """Compute student of done state"""
        student_obj = self.env["student.student"]
        for rec in self:
            rec.student_ids = student_obj.search(
                [
                    ("standard_id", "=", rec.id),
                    ("school_id", "=", rec.school_id.id),
                    ("division_id", "=", rec.division_id.id),
                    ("medium_id", "=", rec.medium_id.id),
                    ("state", "=", "done"),
                ]
            )

    @api.depends("subject_ids")
    def _compute_subject(self):
        """Method to compute subjects."""
        for rec in self:
            rec.total_no_subjects = len(rec.subject_ids)

    @api.depends("student_ids")
    def _compute_total_student(self):
        """Method to compute total student."""
        for rec in self:
            rec.total_students = len(rec.student_ids)

    @api.depends("capacity", "total_students")
    def _compute_remain_seats(self):
        """Method to compute remaining seats."""
        for rec in self:
            rec.remaining_seats = rec.capacity - rec.total_students

    school_id = fields.Many2one(
        "school.school",
        "School",
        required=True,
        help="School of the following standard",
    )
    standard_id = fields.Many2one(
        "standard.standard", "Standard", required=True, help="Standard"
    )
    division_id = fields.Many2one(
        "standard.division",
        "Division",
        required=True,
        help="Standard division",
    )
    medium_id = fields.Many2one(
        "standard.medium",
        "Medium",
        required=True,
        help="Medium of the standard",
    )
    subject_ids = fields.Many2many(
        "subject.subject",
        "subject_standards_rel",
        "subject_id",
        "standard_id",
        "Subject",
        help="Subjects of the standard",
    )
    user_id = fields.Many2one(
        "school.teacher", "Class Teacher", help="Teacher of the standard"
    )
    student_ids = fields.One2many(
        "student.student",
        "standard_id",
        "Student In Class",
        compute="_compute_student",
        store=True,
        help="Students which are in this standard",
    )
    color = fields.Integer("Color Index", help="Index of color")
    cmp_id = fields.Many2one(
        "res.company",
        "Company Name",
        related="school_id.company_id",
        store=True,
        help="Company_id of the school",
    )
    syllabus_ids = fields.One2many(
        "subject.syllabus",
        "standard_id",
        "Syllabus",
        help="Syllabus of the following standard",
    )
    total_no_subjects = fields.Integer(
        "Total No of Subject",
        compute="_compute_subject",
        help="Total subjects in the standard",
    )
    name = fields.Char("Name", help="Standard name")
    capacity = fields.Integer("Total Seats", help="Standard capacity")
    total_students = fields.Integer(
        "Total Students",
        compute="_compute_total_student",
        store=True,
        help="Total students of the standard",
    )
    remaining_seats = fields.Integer(
        "Available Seats",
        compute="_compute_remain_seats",
        store=True,
        help="Remaining seats of the standard",
    )
    class_room_id = fields.Many2one(
        "class.room", "Room Number", help="Class room of the standard"
    )

    @api.onchange("standard_id", "division_id")
    def onchange_combine(self):
        """Onchange to assign name respective of it's standard and division"""
        self.name = str(self.standard_id.name) + "-" + str(self.division_id.name)

    @api.constrains("standard_id", "division_id")
    def check_standard_unique(self):
        """Method to check unique standard."""
        if self.env["school.standard"].search(
            [
                ("standard_id", "=", self.standard_id.id),
                ("division_id", "=", self.division_id.id),
                ("school_id", "=", self.school_id.id),
                ("id", "not in", self.ids),
            ]
        ):
            raise ValidationError(_("Division and class should be unique!"))

    # ORM unlink method 
    def unlink(self):
        """Method to check unique standard."""
        for rec in self:
            if rec.student_ids or rec.subject_ids or rec.syllabus_ids:
                raise ValidationError(
                    _(
                        "You cannot delete as it has reference with student,"
                        "subject or syllabus!"
                    )
                )
        return super(SchoolStandard, self).unlink()

    @api.constrains("capacity")
    def check_seats(self):
        """Method to check seats."""
        if self.capacity <= 0:
            raise ValidationError(_("Total seats should be greater than 0!"))

    def name_get(self):
        """Method to display standard and division"""
        return [
            (rec.id, rec.standard_id.name + "[" + rec.division_id.name + "]")
            for rec in self
        ]
