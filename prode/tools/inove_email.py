import re
import traceback

from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from django.template.loader import get_template


class MesiSmtp():
    def __init__(self):
        self.username = "AKIAXPS52PN4S35RKO4R"
        self.password = "BDsfj1THDx0BnPNdkN8xhAQBZUbKp+B09oOGLerX2agd"
        self.smtp = "email-smtp.us-east-1.amazonaws.com"
        self.port = 587
        self.use_tls = True


class EmailGeneric():
    def __init__(self, from_email):
        self.smtp_service = MesiSmtp()
        self.from_email = from_email

    def send(self, email_data, to_email, hide_emails=False):
        try:
            with get_connection(
                host=self.smtp_service.smtp,
                port=self.smtp_service.port,
                username=self.smtp_service.username,
                password=self.smtp_service.password,
                use_tls=self.smtp_service.use_tls
            ) as connection:
                if hide_emails == False:
                    to = to_email
                    bcc = []
                else:
                    to = []
                    bcc = to_email

                # Reemplazar saltos de linea HTML por saltos de linea en texto
                email_data['message'] = email_data['message'].replace('<br>', '\n')
                # Quitar código HTML
                email_data['message'] = re.sub(re.compile('<.*?>'), '', email_data['message'])

                msg = EmailMessage(email_data['title'], email_data['message'], self.from_email, to=to, bcc=bcc, connection=connection)
                msg.send()
                return True
        except:
            print("Error al enviar mail")
            print(traceback.format_exc())
            return False


def send_generic_email(sender, to_emails, title, message, hide_emails=False):
    email_data = {}
    email_data["title"] = title
    email_data["message"] = message
    return EmailGeneric(sender).send(email_data, to_emails, hide_emails)
