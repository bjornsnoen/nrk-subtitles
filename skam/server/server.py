""" Nrk subs fastapi app """

from typing import Union

from fastapi import FastAPI

from skam.scraper.show.show import get_show

from .responses.episode import SubtitlesModel, episode_model_from_episode
from .responses.show import (
    ShowListModel,
    ShowModel,
    get_show_list,
    show_model_from_show,
)

app = FastAPI()


@app.get("/shows", response_model=ShowListModel)
async def shows():
    """ Fetch list of shows """
    return get_show_list()


@app.get("/show/{show_name}", response_model=ShowModel)
async def show(show_name: str):
    """ Fetch show info by show slug """
    show = get_show(show_name)
    return show_model_from_show(show)


@app.get(
    "/show/{show_name}/season/{season_name}/episode/{episode_number}",
    response_model=SubtitlesModel,
)
async def subs(
    show_name: str, season_name: Union[str, int], episode_number: Union[str, int]
):
    """ Fetch subs for specific episode """
    show = get_show(show_name)
    current_episode = show.get_episode(season_name, episode_number)
    next_episode = show.get_following_episode(current_episode)
    previous_episode = show.get_preceding_episode(current_episode)

    return SubtitlesModel(
        episode=episode_model_from_episode(current_episode),
        next_episode=episode_model_from_episode(next_episode) if next_episode else None,
        previous_episode=episode_model_from_episode(previous_episode)
        if previous_episode
        else None,
        subs=current_episode.get_subs(),
    )
