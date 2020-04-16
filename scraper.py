#! /usr/bin/env python
import requests
from bs4 import BeautifulSoup as bs
import json
import re
import webvtt
from io import StringIO
from typing import List
import dateparser
from functools import reduce

class Show:

    config = False

    def __init__(self, series):
        self.config = self.get_config(series)

    def get_config(self, series):
        if self.config:
            return self.config
        link = "https://tv.nrk.no/serie/" + series
        r = requests.get(link)
        text = r.text
        soup = bs(text, "html5lib")
        all_scripts = soup.findAll('script')
        for script_tag in all_scripts:
            try:
                text = script_tag.get_text().replace('undefined', 'null')
                start = text.index('initialState') - 2

                end = text.find(';')
                full_object = text[start:end]

                as_json = json.loads(full_object)

                return as_json['initialState']
            except:
                continue
        raise Exception("No initialState found")

    def get_seasons(self):
        return self.config['series']['seasons']

    def get_episodes_in_season(self, number):
        try:
            season = self.config['series']['seasons'][number]
            return season['episodes']
        except IndexError:
            # God damn it NRK, just because you run one every year doesn't mean you can just not give me the season number
            for season in self.config['series']['seasons']:
                if season['name'].isnumeric() and int(season['name']) == number:
                    instalments = list(filter(lambda instalment: instalment['season']['name'] == season['name'], self.config['standard']['instalments']['instalments']))
                    return instalments

    def get_episode(self, season, episode):
        try:
            season = self.get_seasons()[season]
            return season['episodes'][episode]
        except:
            episodes = self.get_episodes_in_season(season)
            episode = reduce((lambda episode_x, episode_y: episode_x if dateparser.parse(episode_x['titles']['title']).timestamp() == episode else episode_y), episodes)
            return episode

    def get_subs_for_episode(self, season, episode):
        episode = self.get_episode(season, episode)
        id = episode['prfId']
        prefix = id[0:6]
        dir = id[6:8]
        link = "https://undertekst.nrk.no/prod/{prefix}/{dir}/{prfid}/{LANG}/{prfid}.vtt"
        real_link = link.format(prfid=id, prefix=prefix, dir=dir, LANG="TTV")
        r = requests.get(real_link)
        if r.status_code != 200:
            real_link = link.format(prfid=id, prefix=prefix, dir=dir, LANG="NOR")
            r = requests.get(real_link)
        return self.parse_subs(r.text)

    def parse_subs(self, subs):
        buffer = StringIO(subs)
        lines = []
        for caption in webvtt.read_buffer(buffer):
            lines.append(caption.text.encode('latin-1').decode())
        return lines

    def get_episode_titles(self, season, episode):
        episode = self.get_episode(season, episode)
        return episode['titles']

class Nrk:

    def get_series(self):
        url = "https://tv.nrk.no"
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')
        series = []
        for a in soup.findAll('a'):
            if a['href'].find('/serie/') == 0:
                serie = a['href'].replace('/serie', "")
                if (serie.rfind('/') != 0):
                    serie = re.search(r'(?<=/)(.*)(?=/)', serie)
                else:
                    serie = re.search(r'(?<=/)(.*)', serie)
                try:
                    serie = serie.group()
                    series.index(serie)
                except:
                    if not serie:
                        continue
                    series.append(serie)
        series = sorted(series)
        return series


class ShowLink:
    def __init__(self, name: str, link: str):
        self.name = name
        self.link = link


class Section:
    def __init__(self, name: str):
        self.name = name
        self.show_links = {}

    def add(self, show_link: ShowLink):
        self.show_links[show_link.name] = show_link
    
    def get_shows(self) -> List[ShowLink]:
        return self.show_links.values()


class Catalog:
    def __init__(self, links: List[ShowLink]):
        self.links = links
        self.sections = {}
    
    def get_sections(self) -> List[Section]:
        if not self.sections.__len__():
            for link in self.links:
                first_letter = link.name[0].lower()
                if not first_letter in self.sections:
                    self.sections[first_letter] = Section(first_letter.upper())
                
                self.sections[first_letter].add(link)
                
        return self.sections.values()
        

