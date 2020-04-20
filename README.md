## Overview

This is sample django project built by Roman Fedorov (rfedorov@linkentools.com). 
It has been requested by HR.

## Original Requirements

Hey Roman,

It's ***, HR at *** team. I'm sending our code challenge. 
There is no max or min time for it, but the usual range is about 5-7 hours. 
The deadline for the code challenge will be ***, but feel free to let me know if you need some more time.

In terms of our task, we would like you to:

1. Create a new web application using Django

2. Scrape the Ticketmaster Discovery API for events
https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
Don’t scrape everything. 50 pages should be enough because of API keys are limited by 5k requests per day.

3. Store and/or structure the events that you scrape into your Django application. Event should have at least: event name, promoter name if it exists, description, multiple prices, url, start date, finish date)

4. Inside your Django app, create a searchable api endpoint (returns json) allow the api request to search for event name, event start date, promoter name, ticket cost (min and max for a standard price).

5. Inside your application, create 1 API endpoint that accepts json that allows a user to update the locally stored event record, create some arbitrary validations.

6. Send us the code and the URL to your hosted application.

7. Write Tests you find necessary

Ticketmaster API key: ***
Please let us know in case you experience any issues with this.
Looking forward to hearing from you!

## Blocks

This project based on wms [`django template`](README_wms.md):

- Always up-to-date with the help of [`@dependabot`](https://dependabot.com/)
- Supports latest `python3.7+`
- [`poetry`](https://github.com/python-poetry/poetry) for managing dependencies
- [`mypy`](https://mypy.readthedocs.io) and [`django-stubs`](https://github.com/typeddjango/django-stubs) for static typing
- [`pytest`](https://pytest.org/) and [`hypothesis`](https://github.com/HypothesisWorks/hypothesis) for unit tests
- [`flake8`](http://flake8.pycqa.org/en/latest/) and [`wemake-python-styleguide`](https://wemake-python-styleguide.readthedocs.io/en/latest/) for linting
- [`docker`](https://www.docker.com/) for development, testing, and production
- [`Gitlab CI`](https://about.gitlab.com/gitlab-ci/) with full `build`, `test`, and `deploy` pipeline configured by default

Primary Python libraries:

- `django` 2.2.12 (main framework)
- `djangorestframework` (json REST API)
- `djangorestframework-filters` (powerful filters)
- `pytest-vcr` (save API output in cassettes for tests)
- `tqdm` (display download progress)
- `jsonschema` (validate input json)

## Project Structure

[`server/apps/main`](server/apps/main) - django root

[`server/apps/main/event`](server/apps/main/event) - primary event logic

[`server/apps/main/management/commands/get_events.py`](server/apps/main/management/commands/get_events.py) - download event logic

[`server_tests`](server_tests) - all tests here

[`server_tests/test_apps/test_main/test_event`](server_tests/test_apps/test_main/test_event) - event tests

[`server_tests/test_apps/test_main/test_event/cassettes/test_get_events.yaml`](server_tests/test_apps/test_main/test_event/cassettes/test_get_events.yaml) - event cassettes, prevent real API calls in tests 

## Web interface

[`https://ticket.rfedorov.ru/api/event/`](https://ticket.rfedorov.ru/api/event/) 

primary url with deployed version

[`/admin/main/event/`](https://ticket.rfedorov.ru/admin/main/event/)
 
list all Events in default django admin

[`/api/event/G5vVZ4U9eCe11/`](https://ticket.rfedorov.ru/api/event/G5vVZ4U9eCe11/)

View/Edit/Delete Event with id `G5vVZ4U9eCe11`

[`/api/event/?limit=20&offset=20&cost_min__lte=50&name__contains=Seattle`](https://ticket.rfedorov.ru/api/event/?limit=20&offset=20&cost_min__lte=50&name__contains=Seattle)

simple filter with sql equivalent `cost_min <= 50 and name like %Seattle%`

[`/api/event/?limit=20&offset=20&cost_min__lte=50&promoter_name__contains=REGULAR&name__regex=York&start_date__hour=23`](https://ticket.rfedorov.ru/api/event/?limit=20&offset=20&cost_min__lte=50&promoter_name__contains=REGULAR&name__regex=York&start_date__hour=23)

filter Events according next logic:
- `cost_min` <= `50`
- `promoter_name` contains text `REGULAR`
- `name` regex match `York`
- `start_date` get hour `23`

## Filters
[django documentation](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#field-lookups)

Supported filters:
- exact
- iexact
- contains
- icontains
- in
- gt
- gte
- lt
- lte
- startswith
- istartswith
- endswith
- iendswith
- range
- date
- year
- iso_year
- month
- day
- week
- week_day
- quarter
- time
- hour
- minute
- second
- isnull
- regex
- iregex
