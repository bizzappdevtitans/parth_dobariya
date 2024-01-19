from odoo import models, fields, api
from datetime import datetime


class SchoolManagement(models.Model):
    _name = "school.management"
    _description = "school_management"

    student_name = fields.Char(string="Name")
    student_roll = fields.Integer(string="ROll no.")
    student_modile = fields.Integer(string="Mobile no.")
    student_count = fields.Integer(string="Count")
    student_age = fields.Integer(string="Age", compute="_compute_age")
    student_address = fields.Char(string="Address")
    student_gender = fields.Selection(
        [("Male", "Male"), ("Female", "Female")], string="Gender"
    )
    student_birth_date = fields.Datetime(string="Birth Date")
    student_description = fields.Text(string="Description")

    def action_view_student(self):
        print("\n\n\n helloooooooooooooooooooooooooooo")

    def button_in_confirm(self):
        print("\n\n\n Confirm button Called")

    def _compute_course_count(self):
        for res in self:
            course_count = self.env["course.course"].search_count(
                [("teacher_id", "=", res.id)]
            )
            res.course_count = course_count

    def action_course_detail(self):
        print("\n\n\n Course Detail")
