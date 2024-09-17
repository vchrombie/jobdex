# scraper/apple.py

from ..scraper import scraper
from ..utils import is_today


@scraper('apple')
def parse_apple(soup):
    """
    Scraper function for Apple Careers website.
    """

    # Find the table containing job listings
    table = soup.find('table', class_='table--advanced-search')
    if not table:
        return  # No table found

    # Iterate over all <tr> elements in the table
    for row in table.find_all('tr'):
        # Find the first table data cell
        td = row.find('td', class_='table-col-1')
        if not td:
            continue

        # Extract the position name and URL
        a_tag = td.find('a', class_='table--advanced-search__title')
        if a_tag:
            position_name = a_tag.get_text(strip=True)
            url = a_tag.get('href')
            # Prepend the base URL if needed
            if url and not url.startswith('http'):
                url = 'https://jobs.apple.com' + url
        else:
            continue  # Skip if no link found

        # Extract the date
        date_elem = td.find('span', class_='table--advanced-search__date')
        if date_elem:
            date_str = date_elem.get_text(strip=True)
        else:
            continue  # Skip if no date found

        # Check if the job was posted today
        if is_today(date_str, '%b %d, %Y'):
            yield {
                'position_name': position_name,
                'url': url,
                'date_posted': date_str
            }
