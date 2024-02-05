# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _

EM = r"[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"


def emailvalidation(email):
    """Check valid email."""
    if email:
        email_regex = re.compile(EM)
        if not email_regex.match(email):
            raise ValidationError(
                _(
                    """This seems not to be valid email.
Please enter email in correct format!"""
                )
            )


class StandardMedium(models.Model):
    """Defining a medium(ENGLISH, HINDI, GUJARATI) related to standard"""

    _name = "standard.medium"
    _description = "Standard Medium"
    _order = "sequence"

    sequence = fields.Integer("Sequence", required=True, help="Sequence of the record")
    name = fields.Char("Name", required=True, help="Medium of the standard")
    code = fields.Char("Code", required=True, help="Medium code")
    description = fields.Text("Description", help="Description")


class StandardStandard(models.Model):
    """Defining Standard Information."""

    _name = "standard.standard"
    _description = "Standard Information"
    _order = "sequence"

    sequence = fields.Integer("Sequence", required=True, help="Sequence of the record")
    name = fields.Char("Name", required=True, help="Standard name")
    code = fields.Char("Code", required=True, help="Code of standard")
    description = fields.Text("Description", help="Description")

    @api.model
    def next_standard(self, sequence):
        """This method check sequence of standard"""
        stand_rec = self.search([("sequence", ">", sequence)], order="id", limit=1)
        return stand_rec and stand_rec.id or False


class SubjectElective(models.Model):
    """Defining Subject Elective"""

    _name = "subject.elective"
    _description = "Elective Subject"

    name = fields.Char("Name", help="Elective subject name")
    subject_ids = fields.One2many(
        "subject.subject",
        "elective_id",
        "Elective Subjects",
        help="Subjects of the respective elective subject",
    )


class AttendanceType(models.Model):
    """Defining attendance type."""

    _name = "attendance.type"
    _description = "School Type"

    name = fields.Char("Name", required=True, help="Attendance type name")
    code = fields.Char("Code", required=True, help="Attendance type code")


class StudentDescription(models.Model):
    """Defining a Student Description"""

    _name = "student.description"
    _description = "Student Description"

    des_id = fields.Many2one(
        "student.student", "Student Ref.", help="Student record from students"
    )
    name = fields.Char("Name", help="Description name")
    description = fields.Char("Description", help="Student description")


class StudentDescipline(models.Model):
    """Definign student dscipline."""

    _name = "student.descipline"
    _description = "Student Discipline"

    student_id = fields.Many2one("student.student", "Student", help="Student")
    teacher_id = fields.Many2one(
        "school.teacher", "Teacher", help="Teacher who examine the student"
    )
    date = fields.Date("Date", help="Date")
    class_id = fields.Many2one("standard.standard", "Class", help="Class of student")
    note = fields.Text("Note", help="Discipline Note")
    action_taken = fields.Text("Action Taken", help="Action taken against discipline")


class StudentHistory(models.Model):
    """Defining Student History."""

    _name = "student.history"
    _description = "Student History"

    student_id = fields.Many2one("student.student", "Student", help="Related Student")
    academice_year_id = fields.Many2one(
        "academic.year", "Academic Year", help="Academice Year"
    )
    standard_id = fields.Many2one(
        "school.standard", "Standard", help="Standard of the following student"
    )
    percentage = fields.Float(
        "Percentage", readonly=True, help="Percentage of the student"
    )
    result = fields.Char("Result", readonly=True, help="Result of the student")


class StudentCertificate(models.Model):
    """Defining student certificate."""

    _name = "student.certificate"
    _description = "Student Certificate"

    student_id = fields.Many2one("student.student", "Student", help="Related student")
    description = fields.Char("Description", help="Description")
    certi = fields.Binary("Certificate", required=True, help="Student certificate")


class StudentReference(models.Model):
    """Defining a student reference information"""

    _name = "student.reference"
    _description = "Student Reference"

    reference_id = fields.Many2one(
        "student.student", "Student", help="Student reference"
    )
    name = fields.Char("First Name", required=True, help="Student name")
    middle = fields.Char("Middle Name", required=True, help="Student middle name")
    last = fields.Char("Surname", required=True, help="Student last name")
    designation = fields.Char("Designation", required=True, help="Student designation")
    phone = fields.Char("Phone", required=True, help="Student phone")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")],
        "Gender",
        help="Student gender",
    )


class AcademicSubject(models.Model):
    """Defining a student previous school information"""

    _name = "academic.subject"
    _description = "Student Previous School"

    add_sub_id = fields.Many2one(
        "student.previous.school",
        "Add Subjects",
        invisible=True,
        help="Select student previous school",
    )
    name = fields.Char("Name", required=True, help="Enter previous school name")
    maximum_marks = fields.Integer("Maximum marks", help="Enter maximum mark")
    minimum_marks = fields.Integer("Minimum marks", help="Enter minimum marks")


class StudentRelationMaster(models.Model):
    """Student Relation Information"""

    _name = "student.relation.master"
    _description = "Student Relation Master"

    name = fields.Char("Name", required=True, help="Enter Relation name")
    seq_no = fields.Integer("Sequence", help="Relation sequence")


class GradeMaster(models.Model):
    """Defining grade master."""

    _name = "grade.master"
    _description = "Grade Master"

    name = fields.Char("Grade", required=True, help="Grade name")
    grade_ids = fields.One2many(
        "grade.line",
        "grade_id",
        "Grade Lines",
        help="Grade which are consider in this.",
    )


class ClassRoom(models.Model):
    """Defining class room."""

    _name = "class.room"
    _description = "Class Room"

    name = fields.Char("Name", help="Class room name")
    number = fields.Char("Room Number", help="Class room number")


class Report(models.Model):
    _inherit = "ir.actions.report"

    def render_template(self, template, values=None):
        student_id = self._context.get("student_id")
        if student_id:
            student_rec = self.env["student.student"].browse(student_id)
        if student_rec and student_rec.state == "draft":
            raise ValidationError(
                _("You cannot print report forstudent in unconfirm state!")
            )
        return super(Report, self).render_template(template, values)
