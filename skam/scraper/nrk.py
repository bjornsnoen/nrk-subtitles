""" Fetcher for all online series from nrk.no """
import re

import requests
from bs4 import BeautifulSoup as bs  # type: ignore


def get_series():
    """ Get all series we can find on NRK """
    url = "https://tv.nrk.no"
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    series = []
    for hyperlink in soup.findAll("a"):
        if hyperlink["href"].find("/serie/") == 0:
            serie = hyperlink["href"].replace("/serie", "")
            if serie.rfind("/") != 0:
                serie = re.search(r"(?<=/)(.*)(?=/)", serie)
            else:
                serie = re.search(r"(?<=/)(.*)", serie)
            try:
                serie = serie.group()
                series.index(serie)
            except:
                if not serie:
                    continue
                series.append(serie)

    series = sorted(series)
    return series
