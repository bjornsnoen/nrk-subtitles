""" Module containing pydantic response model for episodes """
from typing import List, Optional, Union

# pylint: disable=no-name-in-module
from pydantic import BaseModel

from subtitles.scraper.episode.episode import Episode


class EpisodeModel(BaseModel):
    """ Pydantic model for episodes """

    episode: str
    number: Union[str, int]
    season: Union[str, int]
    subtitle: Optional[str] = None
    image_url: Optional[str] = None
    available: bool = False


class SubtitlesModel(BaseModel):
    """ Pydantic mode for subtitles with context episodes"""

    episode: EpisodeModel
    previous_episode: Optional[EpisodeModel]
    next_episode: Optional[EpisodeModel]
    subs: Optional[List[str]]


def episode_model_from_episode(
    episode: Episode, season: Union[str, int]
) -> EpisodeModel:
    """ Function to create pydantic episode model from normal episode instance """
    return EpisodeModel(
        episode=episode.title,
        number=episode.episode_number,
        subtitle=episode.subtitle,
        image_url=episode.image_url,
        available=episode.available,
        season=season,
    )
