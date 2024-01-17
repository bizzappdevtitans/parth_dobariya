from odoo import api, fields, models


class CourseDetails(models.Model):
    _name = "course.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Course Detail"

    teacher_id = fields.Many2one("teacher.detail", ondelete="cascade", string="Teacher")
    course_name = fields.Char(string="Course Name", required=True)
    course_upload_date = fields.Datetime(
        string="Upload Date", default=fields.Datetime.now
    )
    first_name = fields.Char(string="First Name", related="teacher_id.first_name")
    reference = fields.Char(string="Reference")
    description = fields.Html(string="Description")
    teacher_count = fields.Integer(
        string="Teacher Count",
    )

    priority = fields.Selection(
        [
            ("0", "Normal"),
            ("1", "Low"),
            ("2", "High"),
            ("3", "Very High"),
        ],
        string="Priority",
    )
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_process", "In Process"),
            ("cancle", "cancle"),
            ("done", "Done"),
        ],
        string="Status",
        default="draft",
        required=True,
    )

    @api.onchange("teacher_id")
    def onchange_teacher_id(self):
        self.reference = self.teacher_id.first_name

    def object_button(self):
        print("Button clicked")