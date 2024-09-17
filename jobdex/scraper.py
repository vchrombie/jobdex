# scraper.py

# Registry to hold scraper functions
SCRAPERS = {}


def scraper(name):
    """
    Decorator for a scraper function.
    """
    def decorator(func):
        SCRAPERS[name] = func
        return func
    return decorator
