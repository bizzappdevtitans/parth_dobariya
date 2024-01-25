# import time
import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class StudentNews(models.Model):
    """Defining studen news."""

    _name = "student.news"
    _description = "Student News"
    _rec_name = "subject"
    _order = "date asc"

    subject = fields.Char("Subject", required=True, help="Subject of the news.")
    description = fields.Text("Description", help="Description")
    date = fields.Datetime("Expiry Date", help="Expiry date of the news.")
    user_ids = fields.Many2many(
        "res.users",
        "user_news_rel",
        "id",
        "user_ids",
        "User News",
        help="Name to whom this news is related.",
    )
    color = fields.Integer("Color Index", default=0, help="Color index")

    @api.constrains("date")
    def checknews_dates(self):
        """Check news date."""
        new_date = fields.datetime.today()
        if self.date < new_date:
            raise ValidationError(_("Configure expiry date greater than current date!"))

    def news_update(self):
        """Method to send email to student for news update"""
        emp_obj = self.env["hr.employee"]
        obj_mail_server = self.env["ir.mail_server"]
        user = self.env.user
        # Check if out going mail configured
        mail_server_record = obj_mail_server.search([], limit=1)
        if not mail_server_record:
            raise UserError(
                _(
                    """User Email Configuration!
"Outgoing mail server not specified!"""
                )
            )
        email_list = []
        # Check email is defined in student
        for news in self:
            if news.user_ids and news.date:
                email_list = [
                    news_user.email for news_user in news.user_ids if news_user.email
                ]
                if not email_list:
                    raise UserError(
                        _(
                            """User Email Configuration!,
Email not found in users!"""
                        )
                    )
            # Check email is defined in user created from employee
            else:
                for employee in emp_obj.search([]):
                    if employee.work_email:
                        email_list.append(employee.work_email)
                    elif employee.user_id and employee.user_id.email:
                        email_list.append(employee.user_id.email)
                if not email_list:
                    raise UserError(
                        _(
                            """Email Configuration!,
Email not defined!"""
                        )
                    )
            news_date = news.create_date
            # Add company name while sending email
            company = user.company_id.name or ""
            body = """Hi,<br/><br/>
                    This is a news update from <b>{}</b> posted at {}<br/>
                    <br/> {} <br/><br/>
                    Thank you.""".format(
                company,
                news_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                news.description or "",
            )
            smtp_user = mail_server_record.smtp_user or False
            # Check if mail of outgoing server configured
            if not smtp_user:
                raise UserError(
                    _(
                        """Email Configuration,
Kindly,Configure Outgoing Mail Server!"""
                    )
                )
            notification = "Notification for news update."
            # Configure email
            message = obj_mail_server.build_email(
                email_from=smtp_user,
                email_to=email_list,
                subject=notification,
                body=body,
                body_alternative=body,
                reply_to=smtp_user,
                subtype="html",
            )
            # Send Email configured above with help of send mail method
            obj_mail_server.send_email(
                message=message, mail_server_id=mail_server_record.id
            )
        return True
