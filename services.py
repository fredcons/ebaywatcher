from jinja2 import Environment, FileSystemLoader
import yaml
import sendgrid
import os
import re
from datetime import datetime, timedelta
from sendgrid.helpers.mail import Mail, Email, Content
from model import SearchDefinition, EmailConfig, SearchConfig, Config
from terminaltables import SingleTable


class MailFormatter:

    @staticmethod
    def format_results(results):
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('mail.html.j2')
        return template.render(results=results)


class SearchDefinitionLoader:

    def __init__(self, search_config):
        self.search_default_category = search_config.search_default_category
        self.search_default_sites = search_config.search_default_sites

    def search_definition_constructor(self, loader, node):
        values = loader.construct_mapping(node)
        text = values["text"]
        use_exact_match = values.get("use_exact_match", True)
        include_description = values.get("include_description", True)
        auction_only = values.get("auction_only", True)
        category = values.get("category", self.search_default_category)
        sites = values.get("sites", self.search_default_sites)
        return SearchDefinition(text, category, sites, use_exact_match, include_description, auction_only)

    def load_definitions(self, search_definitions_path):
        stream = open(search_definitions_path, 'r')
        yaml.add_constructor("!model.SearchDefinition", self.search_definition_constructor)
        search_definitions = yaml.load_all(stream)
        return list(search_definitions)


class ConfigLoader:

    def config_constructor(self, loader, node):
        values = loader.construct_mapping(node)
        env_var_pattern = re.compile(r'^\<%= ENV\[\'(.*)\'\] %\>(.*)$')

        email_from = values["email_from"]
        email_to = values["email_to"]
        email_title = values["email_title"]
        sendgrid_api_key = os.environ.get(env_var_pattern.match(values["sendgrid_api_key"]).groups()[0])
        email_config = EmailConfig(sendgrid_api_key, email_from, email_to, email_title)

        search_default_category = values["search_default_category"]
        search_default_sites = values["search_default_sites"]
        ebay_app_id = os.environ.get(env_var_pattern.match(values["ebay_app_id"]).groups()[0])
        search_config = SearchConfig(ebay_app_id, search_default_category, search_default_sites)

        config = Config(email_config, search_config)

        return config

    def load_config(self, config_path):
        stream = open(config_path, 'r')
        yaml.add_constructor("!model.Config", self.config_constructor)
        config = yaml.load(stream)
        return config


class MailSender:

    def __init__(self, email_config):
        self.sendgrid = sendgrid.SendGridAPIClient(apikey=email_config.sendgrid_api_key)
        self.email_from = email_config.email_from
        self.email_to = email_config.email_to
        self.email_title = email_config.email_title

    def send_mail(self, content):
        from_email = Email(self.email_from)
        to_email = Email(self.email_to)
        subject = self.email_title
        content = Content("text/html", content)
        mail = Mail(from_email, subject, to_email, content)
        self.sendgrid.client.mail.send.post(request_body=mail.get())


class DateFormatter:

    @staticmethod
    def get_start_date(days_back):
        start_date = datetime.today() - timedelta(hours=(days_back * 24) + 3)
        return start_date.strftime("%Y-%m-%dT%H:%M:%S")


class ConsolePrinter:

    @staticmethod
    def print_results(results):
        data = []
        data.append(["Title", "Price", "Category", "End time"])
        for result in results:
            data.append([result.title, result.price + " " + result.currency, result.category_name, result.end_time])
        table = SingleTable(data, title=" %s results found " % (len(results)))
        print(table.table)
