""" Module for the show response model """
from typing import Dict, List, Optional

# pylint: disable=no-name-in-module
from pydantic import BaseModel

from skam.scraper.nrk import get_series
from skam.scraper.show.show import ShowInterface
from skam.server.responses.episode import EpisodeModel, episode_model_from_episode


class ShowModel(BaseModel):
    """ Basic pydantic show model """

    title: str
    season_titles_by_season: Dict[str, Optional[str]]
    episodes_by_season: Dict[str, List[EpisodeModel]]


class ShowListItemModel(BaseModel):
    """ Basic show list item """

    title: str
    slug: str


class ShowListModel(BaseModel):
    """ Basic list of shows """

    shows: List[ShowListItemModel] = []

    def add(self, item: ShowListItemModel):
        """ Add a show to the list """
        self.shows.append(item)


def show_model_from_show(show: ShowInterface) -> ShowModel:
    """ Create a pydantic show model from a standard show interface """
    season_titles_by_season: Dict[str, Optional[str]] = {}
    episodes_by_season: Dict[str, List[EpisodeModel]] = {}
    for season in show.get_available_seasons():
        season_titles_by_season[season] = show.get_season_title(season)
        for episode in show.get_episodes(season):
            if season not in episodes_by_season:
                episodes_by_season[season] = []
            episodes_by_season[season].append(
                episode_model_from_episode(episode, season)
            )

    return ShowModel(
        season_titles_by_season=season_titles_by_season,
        episodes_by_season=episodes_by_season,
        title=show.name,
    )


def get_show_list() -> ShowListModel:
    """ Get a pydantic model containing all known shows """
    shows = ShowListModel()
    for show_slug in get_series():
        item = ShowListItemModel(
            title=show_slug.title().replace("-", " "), slug=show_slug
        )
        shows.add(item)
    return shows
