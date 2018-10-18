#! /usr/bin/env python

from services import MailFormatter, SearchDefinitionLoader, MailSender, DateFormatter
from search import Search
import click


@click.command()
@click.option('--search_definitions_path', default='config/search_definitions.yaml', help='The path to the search definitions file')
@click.option('--num_days', default=1, help='The number of days to get back in time')
@click.option('--mail/--no-mail', default=True)
def run_search(search_definitions_path, num_days, mail):

    print("Running searches defined in %s, going %s days back in time" % (search_definitions_path, num_days))
    search_definition_loader = SearchDefinitionLoader()
    search_definitions = search_definition_loader.load_definitions(search_definitions_path)

    start_date = DateFormatter.get_start_date(num_days)

    search = Search()
    all_results = search.search(start_date, search_definitions)

    if mail:
        print("Sending mail")
        mail = MailFormatter.format_results(all_results)
        mail_sender = MailSender()
        mail_sender.send_mail(mail)


if __name__ == '__main__':
    run_search()
