from odoo import api, fields, models


class CourseCourse(models.Model):
    _name = "course.course"
    _description = "Course Course"

    course_name = fields.Char(string="Course Name")
    course_reference = fields.Char(string="Reference")
    course_description = fields.Html(string="Description")
    course_count = fields.Integer(
        string="Teacher Count", compute="compute_course_count"
    )

    @api.depends("course_name")
    def compute_course_count(self):
        self.course_count = len(self.course_name)

    def action_view_course(self):
        print("\n\n\n Course Name")
