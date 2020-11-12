""" Classes used for scraping nrk and talking to their API """
import requests
import requests_cache

requests_cache.install_cache("scraper")
