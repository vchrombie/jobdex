# scraper.py

import json
import click
import requests

from bs4 import BeautifulSoup

from jobdex.scraper import SCRAPERS
from jobdex.scrapers import *


def load_config(config_file='jobdex/config.json'):
    """
    Load the configuration file.
    """
    with open(config_file) as f:
        return json.load(f)


def scrape_jobs(config):
    """
    Scrape jobs from the webpage, handling pagination.
    """
    click.echo(f"scraping {config['name']} ...\n")

    pagination = config.get('pagination')
    if pagination:
        param_name = pagination.get('param_name', 'page')
        start_page = pagination.get('start', 1)
        max_pages = pagination.get('max_pages', 5)
    else:
        param_name = None
        start_page = 1
        max_pages = 1

    current_page = start_page

    while current_page <= max_pages:
        params = config.get('params', {}).copy()

        if param_name:
            params[param_name] = current_page

        response = requests.get(config['url'], params=params)

        soup = BeautifulSoup(response.content, 'html.parser')

        scraper_function = SCRAPERS.get(config['scraper'])

        if scraper_function is None:
            click.echo(f"No scraper found for {config['name']}.")
            return

        jobs_found = False
        for job in scraper_function(soup):
            yield job
            jobs_found = True

        if not jobs_found:
            # No jobs found on this page, break the loop
            break

        current_page += 1

        if not param_name:
            # If no pagination parameter, process only one page
            break


def find_jobs(config):
    """
    Find jobs from the specific website.
    """
    jobs_today = scrape_jobs(config)

    # Output the results
    count = 0
    for job in jobs_today:
        click.echo(job['position_name'])
        click.echo(job['url'])
        click.echo(job['date_posted'])
        click.echo()

        count += 1

    click.echo(f"found {count} jobs today.")


@click.group()
def main():
    """
    jobdex cli application.
    """
    pass


@main.command()
@click.option('-f', '--find', multiple=True,
              help='Specify the websites to fetch jobs from.')
def fetch(find):
    """
    Fetch jobs from specified websites.
    """

    # Load configuration
    config = load_config()

    sites = list(find) if find else None

    if not sites:
        sites = config.keys()

    for site in sites:
        if site in config:
            find_jobs(config[site])
        else:
            click.echo(f"'{site}' not supported.")


@main.command()
def ls():
    """
    List supported websites to fetch jobs.
    """

    # Load configuration
    config = load_config()

    for site in config.keys():
        click.echo(site)


if __name__ == "__main__":
    main()
