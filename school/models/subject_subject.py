# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class SubjectSubject(models.Model):
    """Defining a subject"""

    _name = "subject.subject"
    _description = "Subjects"

    name = fields.Char("Name", required=True, help="Subject name")
    code = fields.Char("Code", required=True, help="Subject code")
    maximum_marks = fields.Integer(
        "Maximum marks", help="Maximum marks of the subject can get"
    )
    minimum_marks = fields.Integer(
        "Minimum marks",
        help="""Required minimum
                                                     marks of the subject""",
    )
    weightage = fields.Integer("WeightAge", help="Weightage of the subject")
    teacher_ids = fields.Many2many(
        "school.teacher",
        "subject_teacher_rel",
        "subject_id",
        "teacher_id",
        "Teachers",
        help="Teachers of the following subject",
    )
    standard_ids = fields.Many2many(
        "standard.standard",
        string="Standards",
        help="""Standards in which the
                                    following subject taught""",
    )
    standard_id = fields.Many2one(
        "standard.standard",
        "Class",
        help="""Class in which the following
                                  subject taught""",
    )
    is_practical = fields.Boolean(
        "Is Practical", help="Check this if subject is practical."
    )
    elective_id = fields.Many2one(
        "subject.elective",
        help="""Elective subject respective
                                  the following subject""",
    )
    student_ids = fields.Many2many(
        "student.student",
        "elective_subject_student_rel",
        "subject_id",
        "student_id",
        "Students",
        help="Students who choose this subject",
    )

    @api.constrains("maximum_marks", "minimum_marks")
    def check_marks(self):
        """Method to check marks."""
        if self.minimum_marks >= self.maximum_marks:
            raise ValidationError(
                _("Configure Maximum marks greater than minimum marks!")
            )

    @api.model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        """Override method to get exam of subject selection."""
        if (
            self._context.get("is_from_subject_report")
            and self._context.get("active_model")
            and self._context.get("active_id")
        ):
            teacher_rec = self.env[self._context.get("active_model")].browse(
                self._context.get("active_id")
            )
            sub_ids = [sub_id.id for sub_id in teacher_rec.subject_id]
            args.append(("id", "in", sub_ids))
        return super(SubjectSubject, self)._search(
            args=args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )
