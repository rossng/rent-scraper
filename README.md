# rent_scraper

This is a collection of scripts designed to scrape property information from the websites of a number of Bristol student letting agencies.

## Requirements

* Python 2.7
* Scrapy 1.0.4

## Running rent_scraper

To run the spiders, just execute the `run.py` module. This will generate a series of `properties_<AGENT NAME>.json` files.

To view the scraped data, run `generate.py`. This will generate the `results.html` page, which lists all of the properties in a human-readable format. 
The webpage uses [List.js](http://www.listjs.com/) for sorting, filtering and searching.