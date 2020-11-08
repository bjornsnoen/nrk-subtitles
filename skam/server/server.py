""" Nrk subs app flask app """
import json

import dateparser
from flask import Flask, render_template, url_for

from ..scraper.catalog import Catalog
from ..scraper.nrk import get_series
from ..scraper.show import Show, ShowLink

app = Flask(__name__)


@app.route("/show/<string:show>/")
def root(show: str):
    """ Home page for series """
    nrk = Show(show)
    seasons = []
    for season in nrk.get_seasons():
        value = {}
        value["episodes"] = []

        if "titles" in season:
            value["title"] = season["titles"]["title"]
        elif "title" in season:
            value["title"] = season["title"]
        else:
            value["title"] = "Ukjent"

        if "seasonNumber" in season:
            value["season_number"] = season["seasonNumber"]
            season_number = season["seasonNumber"]
        elif season["name"].isnumeric():
            value["season_number"] = int(season["name"])
            season_number = int(season["name"])

        episodes = nrk.get_episodes_in_season(season_number)

        for idx, episode in enumerate(episodes, start=0):
            if episode.episode_number:
                number = episode.episode_number - 1
            else:
                date = dateparser.parse(episode.title)
                if date:
                    number = date.timestamp()
                else:
                    number = idx

            episode = nrk.get_episode(season_number, number)
            link = url_for("subs", show=show, season=season_number, episode=number)

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
        title=nrk.config["series"]["titles"]["title"],
    )


@app.route("/show/<string:show>/season/<int:season>/episode/<int:episode>/")
def subs(show, season, episode):
    """ Page for displaying subtitles for a given episde """
    nrk = Show(show)
    try:
        subs = nrk.get_subs_for_episode(season, episode)
    except:
        return render_template("404.html")
    episodes_in_season = nrk.get_episodes_in_season(season)
    if episodes_in_season.__len__() - 1 > episode:
        next = {"season": season, "episode": episode + 1}
    else:
        seasons = nrk.get_seasons()
        if seasons.__len__() > season:
            next = {"season": season + 1, "episode": 0}
        else:
            next = False
    if next:
        next = url_for(
            "subs", show=show, season=next["season"], episode=next["episode"]
        )

    if episode > 0:
        previous = {"season": season, "episode": episode - 1}
    elif (
        "seasonNumber" in nrk.get_season(0)
        and season > nrk.get_season(0)["seasonNumber"]
    ):
        previous = {
            "season": season - 1,
            "episode": nrk.get_episodes_in_season(season - 1)[-1]["episodeNumber"] - 1,
        }
    elif season > 1000 and season > int(nrk.get_season(0)["name"]):
        previous = {
            "season": season - 1,
            "episode": nrk.get_episodes_in_season(season - 1)[-1]["episodeNumber"] - 1,
        }
    else:
        previous = False
    if previous:
        previous = url_for(
            "subs", show=show, season=previous["season"], episode=previous["episode"]
        )

    return render_template(
        "subs.html", subs=subs, next=next, show=show, previous=previous
    )


@app.route("/")
def index():
    """ Home page for flask app """
    links = []
    for series in get_series():
        if not series:
            continue
        link = url_for("root", show=series)
        name = series.title().replace("-", " ")
        links.append(ShowLink(name, link))
    catalog = Catalog(links)

    return render_template("index.html", catalog=catalog)
