""" Module containing nrk catalog classes """
import json
from functools import reduce
from io import StringIO
from typing import List

import dateparser
import requests
import webvtt
from bs4 import BeautifulSoup as bs
from .show import ShowLink


class Section:
    """ Group of shows, probably by first letter in name """

    def __init__(self, name: str):
        self.name = name
        self.show_links = {}

    def add(self, show_link: ShowLink):
        """ Add one show to this section """
        self.show_links[show_link.name] = show_link

    def get_shows(self) -> List[ShowLink]:
        """ Get all shows in section """
        return self.show_links.values()


class Catalog:
    """ Entire catalog of shows """

    def __init__(self, links: List[ShowLink]):
        self.links = links
        self.sections = {}

    def get_sections(self) -> List[Section]:
        """ Get all shows in catalog sorted into sections """
        if not self.sections.__len__():
            for link in self.links:
                first_letter = link.name[0].lower()
                if not first_letter in self.sections:
                    self.sections[first_letter] = Section(first_letter.upper())

                self.sections[first_letter].add(link)

        return self.sections.values()
