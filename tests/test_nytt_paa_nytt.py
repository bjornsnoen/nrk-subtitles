from skam.scraper.show import Show

def test_non_episodal_show():
    show = Show('nytt-paa-nytt')
    seasons = show.get_seasons()
    episodes = show.get_episodes_in_season(2020)