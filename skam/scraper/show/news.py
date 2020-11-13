""" Module for news shows """
from typing import List, Optional

from ..episode.episode import Episode
from .standard import StandardShow


class NewsShow(StandardShow):
    """ Class for managing episodes of news shows """

    def __init__(self, config: dict):
        config["standard"] = config["news"]
        super().__init__(config)

    def get_available_seasons(self) -> List[str]:
        available = []
        for season in self.seasons:
            available.append(self._get_season_name_from_config(season))
        return available

    def get_season_title(self, season_number: str) -> Optional[str]:
        for season in self.seasons:
            if season_number == self._get_season_name_from_config(season):
                return season["titles"]["title"]

        return None

    def _find_season_config(self, season_name: str) -> Optional[dict]:
        for season in self.seasons:
            if self._get_season_name_from_config(season) == season_name:
                return season
        return None

    def _get_season_config_by_episode(self, episode: Episode) -> Optional[dict]:
        season_number = self.get_season_number(episode)
        if season_number is None:
            return None
        return self._find_season_config(season_number)

    def _get_season_name_from_config(self, config: dict) -> str:
        url_path = config["_links"]["self"]["href"]
        return url_path.split(sep="/")[-1]

    def get_season_number(self, episode: Episode) -> Optional[str]:
        for season_name, episodes_data in self.episodes_data_by_season.items():
            for potential in self.get_episodes(season_name):
                if potential == episode:
                    return season_name

        return None
