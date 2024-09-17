# scraper.py

import json
import click
import requests

from bs4 import BeautifulSoup

from jobdex.scraper import SCRAPERS
from jobdex.scrapers import *


def scrape_jobs(config):
    """
    Scrape jobs from the webpage, handling pagination.
    """
    print(f"scraping {config['name']} ...\n")

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
            print(f"No scraper found for {config['name']}.")
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
        print(f"position name: {job['position_name']}")
        print(f"url: {job['url']}")
        print(f"date posted: {job['date_posted']}")
        print()

        count += 1

    print(f"found {count} jobs today.")


@click.command()
@click.option('-f', '--fetch', multiple=True, help='specify the websites to fetch jobs')
def main(fetch):

    # Load configuration
    with open('jobdex/config.json') as f:
        config = json.load(f)

    sites = list(fetch) if fetch else None

    if not sites:
        sites = config.keys()

    for site in sites:
        find_jobs(config[site])


if __name__ == "__main__":
    main()
