import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from messages.interfaces import IEmailSender, IMessage, IEmailBuilder, ISmtpClient
from settings import DEFAULT_EMAIL_FROM


class EmailBuilder(IEmailBuilder):
    def set_body_on_message(self, message: ISmtpClient, body: str) -> ISmtpClient:
        message.attach(MIMEText(body, "plain"))
        return message

    def get_message(self, attrs: dict) -> ISmtpClient:
        email_manager = self.get_email_manager()
        body = attrs.pop("body")
        for key, value in attrs.items():
            email_manager[key] = value

        self.set_body_on_message(email_manager, body)
        return email_manager


class SmtpClient(MIMEMultipart, ISmtpClient):
    pass


class Email(
    IMessage,
    IEmailSender,
    EmailBuilder,
):

    def __init__(self, smtp_server, port, password):
        self.port = port
        self.smtp_server = smtp_server
        self.password = password

    def get_email_manager(self):
        return SmtpClient()

    def get_smtp_server(self):
        if not self.smtp_server:
            raise Exception("smtp não definido")
        return self.smtp_server

    def send_email(self, to: list[str], subject: str, body, email_from):
        try:
            message_attrs = {
                "To": to,
                "From": email_from,
                "Subject": subject,
                "body": body,
            }
            message = self.get_message(message_attrs)
            smtp_server = self.get_smtp_server()
            server = smtplib.SMTP(smtp_server, self.port)
            server.starttls()
            server.login(email_from, self.password)
            server.sendmail(email_from, to, message.as_string())
            server.quit()
        except Exception as e:
            print(e)

    def send_message(
        self, to: list[str], subject: str, body, email_from=DEFAULT_EMAIL_FROM
    ):
        self.send_email(to, subject, body, email_from)


class TemplateEmail(
    Email,
):
    def __init__(self, smtp_server, port, password, template_name):
        super().__init__(smtp_server, port, password)
        self.template_path = f"messageService/templates/{template_name}"

    def set_context_body(self, body_context: dict):
        with open(self.template_path, "r") as file:
            content = file.read()
            for key, value in body_context.items():
                concat = "{{" + key + "}}"
                content = content.replace(concat, value)

            return content

    def set_body_on_message(self, message: MIMEMultipart, body_context):
        body = self.set_context_body(body_context)
        return message.attach(MIMEText(body, "html"))

    def send_message(self, to, subject, body_context, email_from=DEFAULT_EMAIL_FROM):
        return super().send_message(to, subject, body_context, email_from)
