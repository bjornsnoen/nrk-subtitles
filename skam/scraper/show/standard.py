""" Class for show that doesn't follow standard season/episode pattern """
from typing import Dict, List, Optional

from ..episode.episode import Episode
from ..episode.standard import StandardEpisode
from .show import NoSuchEpisode, NoSuchSeason, ShowInterface, load_installments


class StandardShow(ShowInterface):
    """ Same as module """

    episodes_data_by_season: Dict[str, List[dict]]

    def __init__(self, config: dict):
        self.episodes_data_by_season = {}
        self.name: str = config["standard"]["titles"]["title"]
        self.subtitle: str = config["standard"]["titles"]["subtitle"]
        self.seasons: List[dict] = config["_embedded"]["seasons"]

        for episode_data in config["_embedded"]["instalments"]["_embedded"][
            "instalments"
        ]:
            self._append_episode_data(episode_data)

    def _append_episode_data(self, episode_data):
        season = episode_data["_links"]["season"]["name"]
        if season not in self.episodes_data_by_season:
            self.episodes_data_by_season[season] = []
        self.episodes_data_by_season[season].append(episode_data)

    def get_available_seasons(self) -> List[str]:
        numbers = []
        for season in self.seasons:
            numbers.append(season["titles"]["title"])

        return numbers

    def get_episodes(self, series_number: str) -> List[Episode]:
        # TODO: Load more episodes if necessary
        episodes: List[Episode] = []
        if series_number not in self.episodes_data_by_season:
            self._load_season_data(series_number)

        for episode_data in self.episodes_data_by_season[series_number]:
            if episode_data["_links"]["season"]["name"] == series_number:
                episodes.append(StandardEpisode(episode_data))

        return episodes

    def _load_season_data(self, series_number: str, page: int = 1):
        season_config = self._find_season_config(str(series_number))
        if season_config is None:
            return
        link = season_config["_links"]["self"]["href"]
        link = link + "?page={page}".format(page=page)
        instalments = load_installments(link)
        for episode_data in instalments["_embedded"]["instalments"]:
            self._append_episode_data(episode_data)

    def _find_season_config(self, season_name: str) -> dict:
        for season in self.seasons:
            if season["titles"]["title"] == season_name:
                return season
        raise NoSuchSeason

    def get_episode(self, season_number, episode_number) -> Episode:
        for episode in self.get_episodes(season_number):
            if episode.episode_number == episode_number:
                return episode
        raise NoSuchEpisode

    def get_preceding_episode(self, current_episode: Episode) -> Optional[Episode]:
        # It's safe to assume that the current_episode will be among the already fetched ones,
        # so let's only look in those. Exception is first episode in season.
        # pylint: disable=unsubscriptable-object
        # ref: https://github.com/PyCQA/pylint/issues/2420
        previous = None
        season_number = self.get_season_number(current_episode)
        if season_number is None:
            return None

        episodes = self.get_episodes(season_number)
        episodes.reverse()
        for episode in episodes:
            if episode == current_episode:
                break
            previous = episode

        if previous is None:
            # First of season
            season_config = self._get_season_config_by_episode(current_episode)
            if season_config is None:
                return None
            preceding_season = self._get_preceding_season(season_config)
            if preceding_season is None:
                return None

            return self.get_episodes(
                self._get_season_name_from_config(preceding_season)
            )[0]

        return previous

    def get_following_episode(self, current_episode: Episode) -> Optional[Episode]:
        season_number = self.get_season_number(current_episode)
        if season_number is None:
            return None

        following = None

        for episode in self.get_episodes(season_number):
            if episode == current_episode:
                break
            following = episode

        if following is None:
            # First of season
            season_config = self._get_season_config_by_episode(current_episode)
            if season_config is None:
                return None
            following_season = self._get_following_season(season_config)
            if following_season is None:
                return None

            return self.get_episodes(
                self._get_season_name_from_config(following_season)
            )[-1]

        return following

    def _get_season_name_from_config(self, config: dict) -> str:
        return config["titles"]["title"]

    def get_season_number(self, episode: Episode) -> str:
        config = self._get_season_config_by_episode(episode)
        return config["titles"]["title"]

    def get_season_title(self, season_number) -> Optional[str]:
        # The one we already have isn't real, it's just the name, but to save requests we'll use it
        season_config = self._get_season_config(season_number)
        if season_config is None:
            return None

        title = season_config["titles"]["title"]
        if season_config["titles"]["subtitle"] is not None:
            title = "{title} {subtitle}".format(
                title=title, subtitle=season_config["titles"]["subtitle"]
            )
        return title

    def _get_preceding_season(self, season_config: dict) -> Optional[dict]:
        preceding = None
        seasons_copy = self.seasons.copy()
        seasons_copy.reverse()
        for season in seasons_copy:
            if season["titles"]["title"] == season_config["titles"]["title"]:
                return preceding
            preceding = season
        return None

    def _get_following_season(self, season_config: dict) -> Optional[dict]:
        # May seem counterintuitive, see above opposite method for context
        # Basically, time flows forward, but we receive the data in reverse, season 0 episode 0 is the last published
        following = None
        for season in self.seasons:
            if season["titles"]["title"] == season_config["titles"]["title"]:
                return following
            following = season
        return None

    def _get_season_config_by_episode(self, episode: Episode) -> dict:
        for season_name, episodes_data in self.episodes_data_by_season.items():
            for episode_data in episodes_data:
                if (
                    episode_data["firstTransmissionDateDisplayValue"]
                    == episode.episode_number
                ):
                    return self._get_season_config(season_name)
        raise NoSuchSeason

    def _get_season_config(self, season_number: str) -> dict:
        for season_config in self.seasons:
            if season_config["titles"]["title"] == season_number:
                return season_config
        raise NoSuchSeason
