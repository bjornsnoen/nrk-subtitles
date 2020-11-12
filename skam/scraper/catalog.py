""" Module containing nrk catalog classes """
from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class ShowLink:
    """ Show name and url """

    name: str
    link: str


class Section:
    """ Group of shows, probably by first letter in name """

    def __init__(self, name: str):
        self.name = name
        self.show_links: Dict[str, ShowLink] = {}

    def add(self, show_link: ShowLink):
        """ Add one episode to this section """
        self.show_links[show_link.name] = show_link

    def get_shows(self) -> Iterable[ShowLink]:
        """ Get all shows in section """
        return self.show_links.values()


class Catalog:
    """ Entire catalog of shows """

    def __init__(self, links: Iterable[ShowLink]):
        self.links = links
        self.sections: Dict[chr, Section] = {}

    def get_sections(self) -> Iterable[Section]:
        """ Get all shows in catalog sorted into sections """
        if not self.sections.__len__():
            for link in self.links:
                first_letter = link.name[0].lower()
                if first_letter not in self.sections:
                    self.sections[first_letter] = Section(first_letter.upper())

                self.sections[first_letter].add(link)

        return self.sections.values()
