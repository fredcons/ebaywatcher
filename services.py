from jinja2 import Environment, FileSystemLoader
import yaml
import sendgrid
import os
from datetime import datetime, timedelta
from sendgrid.helpers.mail import Mail, Email, Content
from model import SearchDefinition


class MailFormatter:

    @staticmethod
    def format_results(results):
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('mail.html.j2')
        return template.render(results=results)


class SearchDefinitionLoader:

    def search_definition_constructor(self, loader, node):
        values = loader.construct_mapping(node)
        text = values["text"]
        use_exact_match = values.get("use_exact_match", True)
        include_description = values.get("include_description", True)
        auction_only = values.get("auction_only", True)
        return SearchDefinition(text, use_exact_match, include_description, auction_only)

    def load_definitions(self, search_definitions_path):
        stream = open(search_definitions_path, 'r')
        yaml.add_constructor("!model.SearchDefinition", self.search_definition_constructor)
        search_definitions = yaml.load_all(stream)
        return list(search_definitions)


class MailSender:

    def __init__(self):
        sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
        self.sendgrid = sendgrid.SendGridAPIClient(apikey=sendgrid_api_key)
        self.from_mail = "frederic.cons@gmail.com"
        self.to_mail = "frederic.cons@gmail.com"

    def send_mail(self, content):
        from_email = Email(self.from_mail)
        to_email = Email(self.to_mail)
        subject = "Vos alertes Ebay"
        content = Content("text/html", content)
        mail = Mail(from_email, subject, to_email, content)
        self.sendgrid.client.mail.send.post(request_body=mail.get())


class DateFormatter:

    @staticmethod
    def get_start_date(days_back):
        start_date = datetime.today() - timedelta(hours=(days_back * 24) + 3)
        return start_date.strftime("%Y-%m-%dT%H:%M:%S")
