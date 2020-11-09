""" TV Show types """
import json
from dataclasses import dataclass
from functools import reduce
from io import StringIO
from typing import Dict, List

import dateparser
import requests
import webvtt
from bs4 import BeautifulSoup as bs
from .episode import Episode


@dataclass
class ShowLink:
    """ Show name and url """

    name: str
    link: str


class Show:
    """ Episodes, seasons, names, etc """

    config = False

    def __init__(self, series: str):
        self.config = self._get_config(series)

    def _get_config(self, series: str):
        """ Fetch the json config from nrk """
        if self.config:
            return self.config
        link = "https://tv.nrk.no/serie/" + series
        response = requests.get(link)
        text = response.text
        soup = bs(text, "html5lib")
        all_scripts = soup.findAll("script")
        for script_tag in all_scripts:
            try:
                text = script_tag.get_text().replace("undefined", "null")
                start = text.index("initialState") - 2

                end = text.find(";")
                full_object = text[start:end]

                as_json = json.loads(full_object)

                return as_json["initialState"]
            except:
                continue
        raise Exception("No initialState found")

    def get_seasons(self):
        """ Retrieve all show seasons """
        return self.config["series"]["seasons"]

    def get_season(self, season_number: int):
        """ Fetch a single season """
        try:
            season = reduce(
                lambda x, y: x if x["seasonNumber"] == season_number else y,
                self.get_seasons(),
            )
        except KeyError:
            season = reduce(
                lambda x, y: x if int(x["name"]) == season_number else y,
                self.get_seasons(),
            )
        return season

    def get_episodes_in_season(self, season_number: int) -> List[Episode]:
        """ Get episodes in season by season number """
        try:
            season = self.get_season(season_number)
            episodes_data = season["episodes"]
        except KeyError:
            # God damn it NRK, just because you run one every year doesn't mean you can just
            # decide not to give me the season number
            for season in self.get_seasons():
                if season["name"].isnumeric() and int(season["name"]) == season_number:
                    instalments = (
                        self.config["series"]["instalments"]
                        if self.config["series"]["instalments"]
                        else self.config["standard"]["instalments"]["instalments"]
                    )
                    instalments_in_season = list(
                        filter(
                            lambda instalment: instalment["season"]["name"]
                            == season["name"],
                            instalments,
                        )
                    )
                    episodes_data = instalments_in_season
                    break

        if episodes_data:
            episodes_data = list(
                filter(
                    lambda episode: episode["availability"]["status"] == "available",
                    episodes_data,
                )
            )
            return list(
                map(
                    lambda episode_data: self._episode_data_to_episode(episode_data),
                    episodes_data,
                )
            )
        return []

    def get_episode(self, season_number: int, episode_number: int) -> Episode:
        """ Get a single episode by season number and episode number """
        try:
            season = self.get_season(season_number)
            episode = self._episode_data_to_episode(season["episodes"][episode_number])
        except:
            episodes = self.get_episodes_in_season(season_number)
            try:
                episode = reduce(
                    (
                        lambda episode_x, episode_y: episode_x
                        if dateparser.parse(" ".join([episode_x.title, str(episode_x.production_year)])).timestamp()
                        == episode_number
                        else episode_y
                    ),
                    episodes,
                )
            except:
                # Last ditch?
                episode = episodes[episode_number]

        return episode

    def _episode_data_to_episode(self, episode_data: dict) -> Episode:
        return Episode(
            episode_data["type"],
            episode_data["prfId"],
            episode_data["titles"]["title"],
            episode_data["titles"]["subtitle"],
            episode_data["episodeNumber"] if "episodeNumber" in episode_data.keys() else None,
            episode_data["productionYear"],
            episode_data["image"][0]["url"],
        )

    def get_subs_for_episode(self, season: int, episode: int) -> List[str]:
        """ Get subs for episode in season, should be removed """
        episode = self.get_episode(season, episode)
        prf_id = episode.prf_id
        prefix = prf_id[0:6]
        dir = prf_id[6:8]
        link = (
            "https://undertekst.nrk.no/prod/{prefix}/{dir}/{prfid}/{LANG}/{prfid}.vtt"
        )
        real_link = link.format(prfid=prf_id, prefix=prefix, dir=dir, LANG="TTV")
        response = requests.get(real_link)
        if response.status_code != 200:
            real_link = link.format(prfid=prf_id, prefix=prefix, dir=dir, LANG="NOR")
            response = requests.get(real_link)
        if response.status_code != 200:
            raise requests.exceptions.InvalidURL
        return self._parse_subs(response.text)

    def _parse_subs(self, subs: str) -> List[str]:
        buffer = StringIO(subs)
        lines = []
        for caption in webvtt.read_buffer(buffer):
            try:
                lines.append(caption.text)
            except:
                pass
        return lines
