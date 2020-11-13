""" Nrk subs app flask app """
from typing import Union

from flask import Flask, render_template, url_for

from ..scraper.catalog import Catalog, ShowLink
from ..scraper.nrk import get_series
from ..scraper.show.show import get_show

app = Flask(__name__)


@app.route("/")
def index():
    """ Home page for flask app """
    links = []
    for series in get_series():
        if not series:
            continue
        link = url_for("root", show_name=series)
        name = series.title().replace("-", " ")
        links.append(ShowLink(name, link))
    catalog = Catalog(links)

    return render_template("index.html", catalog=catalog)


@app.route("/show/<string:show_name>/")
def root(show_name: str):
    """ Home page for series """
    try:
        show = get_show(show_name)
    except Exception as error:
        return error_page()

    seasons = []
    for season in show.get_available_seasons():
        value = {"episodes": []}

        if show.get_season_title(season):
            value["title"] = show.get_season_title(season)

        episodes = show.get_episodes(season)
        episodes = list(filter(lambda episode: episode.available, episodes))

        for idx, episode in enumerate(episodes, start=1):
            if episode.episode_number:
                number = episode.episode_number
            else:
                number = idx

            episode = show.get_episode(season, number)
            link = url_for(
                "subs",
                show_name=show_name,
                season_number=season,
                episode_number=number,
            )

            value["episodes"].append(
                {
                    "title": episode.title,
                    "subtitle": episode.subtitle,
                    "link": link,
                    "image": episode.image_url,
                }
            )

        seasons.append(value)
    return render_template(
        "show-episodes.html",
        seasons=seasons,
        title=show.name,
    )


@app.route("/show/<string:show_name>/season/<season_number>/episode/<episode_number>/")
def subs(
    show_name: str, season_number: Union[str, int], episode_number: Union[int, str]
):
    """ Page for displaying subtitles for a given episode """
    show = get_show(show_name)
    episode = show.get_episode(season_number, episode_number)

    following = show.get_following_episode(episode)
    next_link = (
        url_for(
            "subs",
            show_name=show_name,
            season_number=show.get_season_number(following),
            episode_number=following.episode_number,
        )
        if following is not None and following.available
        else False
    )

    preceding = show.get_preceding_episode(episode)
    previous_link = (
        url_for(
            "subs",
            show_name=show_name,
            season_number=show.get_season_number(preceding),
            episode_number=preceding.episode_number,
        )
        if preceding is not None and preceding.available
        else False
    )

    return render_template(
        "subs.html",
        subs=episode.get_subs(),
        next=next_link,
        show=show_name,
        previous=previous_link,
    )


def error_page():
    """ Common error page function """

    return render_template("404.html")
