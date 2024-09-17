# scraper.py

import click
import requests
from bs4 import BeautifulSoup
import json

from jobdex.scraper import SCRAPERS
from jobdex.scrapers import *


def scrape_jobs(config):
    """
    Scrape jobs from the webpage.
    """
    print(f"scraping {config['name']} ...\n")

    response = requests.get(config['url'], params=config['params'])

    soup = BeautifulSoup(response.content, 'html.parser')

    scraper_function = SCRAPERS.get(config['scraper'])

    if scraper_function is None:
        print(f"No scraper found for {config['name']}.")
        return

    for job in scraper_function(soup):
        yield job


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
