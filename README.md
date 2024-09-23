# jobdex

CLI tool to scrape jobs that are posted today from various job portals

## Usage

```bash
git clone https://github.com/vchrombie/jobdex
cd jobdex
poetry install
poetry shell
jobdex fetch -f apple
```

## Commands

```
$ jobdex --help
Usage: jobdex [OPTIONS] COMMAND [ARGS]...

  jobdex cli application.

Options:
  --help  Show this message and exit.

Commands:
  fetch  Fetch jobs from specified websites.
  ls     List supported websites to fetch jobs.
```

## Roadmap

- [ ] Add scrapers for more websites
  - [ ] microsoft
  - [ ] amazon
  - [ ] netflix
  - [ ] . . .
- [ ] Fetch from websites which use JS/jQuery
- [ ] Add the role as flag, not in the config
- [ ] Add tests

## License

MIT
