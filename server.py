#! /usr/bin/env python

from scraper import Show, Nrk, Catalog, ShowLink
from flask import Flask, render_template, url_for
import json
import dateparser

app = Flask(__name__)

@app.route('/show/<string:show>/')
def root(show):
    nrk = Show(show)
    seasons = []
    for season in nrk.get_seasons():
        value = {}
        value['episodes'] = []

        if 'titles' in season:
            value['title'] = season['titles']['title']
        elif 'title' in season:
            value['title'] = season['title']
        else:
            value['title'] = 'Ukjent'

        if 'seasonNumber' in season:
            value['season_number'] = season['seasonNumber']
            seasonNumber = season['seasonNumber']
        elif season['name'].isnumeric():
            value['season_number'] = int(season['name'])
            seasonNumber = int(season['name'])

        episodes = nrk.get_episodes_in_season(seasonNumber)

        for idx, episode in enumerate(episodes, start=0):
            if 'episodeNumber' in episode:
                number = episode['episodeNumber'] - 1
            else:
                date = dateparser.parse(episode['titles']['title'])
                if date:
                    number = date.timestamp()
                else:
                    number = idx
                
            titles = nrk.get_episode_titles(seasonNumber, number)
            link = url_for('subs',show=show, season=seasonNumber, episode=number)

            value['episodes'].append({
                'title': titles['title'],
                'subtitle': titles['subtitle'],
                'link': link,
                'image': episode['image'][0]
            })

        seasons.append(value)
    return render_template('show-episodes.html', seasons=seasons, title=nrk.config['series']['titles']['title'])

@app.route('/show/<string:show>/season/<int:season>/episode/<int:episode>/')
def subs(show, season, episode):
    nrk = Show(show)
    try:
        subs = nrk.get_subs_for_episode(season, episode)
    except:
        return render_template('404.html')
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
        next = url_for('subs', show=show, season=next['season'], episode=next['episode'])

    if episode > 0:
        previous = {"season": season, "episode": episode - 1}
    elif 'seasonNumber' in nrk.get_season(0) and season > nrk.get_season(0)['seasonNumber']:
        previous = {"season": season - 1, "episode": nrk.get_episodes_in_season(season - 1)[-1]['episodeNumber'] - 1}
    elif season > 1000 and season > int(nrk.get_season(0)['name']):
        previous = {"season": season - 1, "episode": nrk.get_episodes_in_season(season - 1)[-1]['episodeNumber'] - 1}
    else:
        previous = False
    if previous:
        previous = url_for('subs', show=show, season=previous['season'], episode=previous['episode'])

    return render_template('subs.html', subs=subs, next=next, show=show, previous=previous)

@app.route('/')
def test():
    nrk = Nrk()
    links = []
    for series in nrk.get_series():
        if not series:
            continue
        link = url_for('root', show=series)
        name = series.title().replace('-', ' ')
        links.append(ShowLink(name, link))
    catalog = Catalog(links)

    return render_template('index.html', catalog=catalog)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")