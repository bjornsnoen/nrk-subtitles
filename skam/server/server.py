""" Nrk subs fastapi app """

from os import environ
from typing import List, Optional, Union

from fastapi import FastAPI, HTTPException
from requests.exceptions import InvalidURL

from skam.scraper.show.show import NoSuchEpisode, NoSuchSeason, NoSuchShow, get_show

from .responses.episode import SubtitlesModel, episode_model_from_episode
from .responses.show import (
    ShowListModel,
    ShowModel,
    get_show_list,
    show_model_from_show,
)

app = FastAPI(root_path=environ["API_ROOT_PATH"] if "API_ROOT_PATH" in environ else "")


@app.get("/shows", response_model=ShowListModel)
async def shows():
    """ Fetch list of shows """
    return get_show_list()


@app.get("/show/{show_name}", response_model=ShowModel)
async def show(show_name: str):
    """ Fetch show info by show slug """
    try:
        show = get_show(show_name)
    except NoSuchShow:
        raise HTTPException(status_code=404)
    return show_model_from_show(show)


@app.get(
    "/show/{show_name}/season/{season_name}/episode/{episode_number}",
    response_model=SubtitlesModel,
)
async def subs(
    show_name: str, season_name: Union[str, int], episode_number: Union[str, int]
):
    """ Fetch subs for specific episode """
    try:
        show = get_show(show_name)
        current_episode = show.get_episode(season_name, episode_number)
        subs: Optional[List[str]] = current_episode.get_subs()
    except NoSuchShow:
        raise HTTPException(status_code=404, detail="No such show")
    except NoSuchSeason:
        raise HTTPException(status_code=404, detail="No such season")
    except NoSuchEpisode:
        raise HTTPException(status_code=404, detail="No such episode")
    except InvalidURL:
        subs = None
    next_episode = show.get_following_episode(current_episode)
    previous_episode = show.get_preceding_episode(current_episode)

    return SubtitlesModel(
        episode=episode_model_from_episode(current_episode),
        next_episode=episode_model_from_episode(next_episode) if next_episode else None,
        previous_episode=episode_model_from_episode(previous_episode)
        if previous_episode
        else None,
        subs=subs,
    )
