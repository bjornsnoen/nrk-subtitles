""" Episode that follows normal season/episode structure """
from __future__ import annotations

from functools import reduce
from typing import Dict, List, Optional

from skam.scraper.episode.sequential import SequentialEpisode

from ..episode.episode import Episode
from .show import ShowInterface


class SequentialShow(ShowInterface):
    """ Class to represent a normal show """

    def __init__(self, config: dict):
        self.name = config["sequential"]["titles"]["title"]
        self.subtitle = config["sequential"]["titles"]["subtitle"]
        self.seasons: List[Dict] = config["_embedded"]["seasons"]

    def get_available_seasons(self) -> List:
        return list(
            map(lambda season_data: season_data["sequenceNumber"], self.seasons)
        )

    def get_season_title(self, season_number) -> Optional[str]:
        season = reduce(
            lambda data_x, data_y: data_x
            if data_x["sequenceNumber"] == season_number
            else data_y,
            self.seasons,
        )
        if season["sequenceNumber"] == season_number:
            try:
                return ", ".join(season["titles"].values())
            except TypeError:
                return season["titles"]["title"]
        return None

    def get_episodes(self, season_number: int) -> List[Episode]:
        """ Get every episode in the requested season """

        season = None
        for season in self.seasons:
            if season["sequenceNumber"] == season_number:
                break

        if season is None:
            return []

        episodes: List[Episode] = []
        for episode_data in season["_embedded"]["episodes"]:
            episodes.append(SequentialEpisode(episode_data))

        return episodes

    def get_episode(self, season_number: int, episode_number: int) -> Optional[Episode]:
        for episode in self.get_episodes(int(season_number)):
            if episode.episode_number == int(episode_number):
                return episode
        return None

    def get_preceding_episode(self, current_episode: Episode) -> Optional[Episode]:
        previous = None
        for season in self.get_available_seasons():
            for episode in self.get_episodes(season):
                if episode == current_episode:
                    return previous
                previous = episode

        return previous

    def get_following_episode(self, current_episode: Episode) -> Optional[Episode]:
        return_next = False
        for season in self.get_available_seasons():
            for episode in self.get_episodes(season):
                if return_next:
                    return episode
                if episode == current_episode:
                    return_next = True

        return None

    def get_season_number(self, episode: Episode) -> Optional[int]:
        for season in self.get_available_seasons():
            if self.season_has_episode(season, episode):
                return season

        return None

    def season_has_episode(self, season_number: int, episode: Episode) -> bool:
        """ Inherit """
        for potential in self.get_episodes(season_number):
            if potential == episode:
                return True

        return False
