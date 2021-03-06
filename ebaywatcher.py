#! /usr/bin/env python

from services import MailFormatter, SearchDefinitionLoader, ConfigLoader, MailSender, DateFormatter, ConsolePrinter
from search import Search
import click


@click.command()
@click.option('--config_path', default='config/config.yaml', help='The path to the config file')
@click.option('--search_definitions_path', default='config/search_definitions.yaml', help='The path to the search definitions file')
@click.option('--num_days', default=1, help='The number of days to get back in time')
@click.option('--mail/--no-mail', default=True, help="Whether to send an email or not. If not, results wil be printed to the console")
def run_search(config_path, search_definitions_path, num_days, mail):

    print("Running searches defined in %s, going %s days back in time, with %s" % (search_definitions_path, num_days, config_path))

    config_loader = ConfigLoader()
    config = config_loader.load_config(config_path)

    search_definition_loader = SearchDefinitionLoader(config.search_config)
    search_definitions = search_definition_loader.load_definitions(search_definitions_path)

    start_date = DateFormatter.get_start_date(num_days)

    search = Search(config.search_config)
    results = search.search(start_date, search_definitions)

    if mail:
        mail_content = MailFormatter.format_results(results)
        mail_sender = MailSender(config.email_config)
        mail_sender.send_mail(mail_content)
    else:
        ConsolePrinter.print_results(results)


if __name__ == '__main__':
    run_search()
