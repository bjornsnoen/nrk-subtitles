from skam.scraper.show.show import get_show

SHOW_NAME = "nytt-paa-nytt"


def test_get_season_one():
    show = get_show(SHOW_NAME)
    episodes = show.get_episodes("2020")
    # Always 10 per page
    assert len(episodes) == 10


def test_get_all_seasons():
    show = get_show(SHOW_NAME)
    seasons = show.get_available_seasons()
    assert len(seasons) == 11


def test_get_known_episode_of_show():
    show = get_show(SHOW_NAME)
    episode = show.get_episode("2020", "13.11.2020")
    assert episode.episode_number == "13.11.2020"


def test_get_first_episode_of_show():
    show = get_show(SHOW_NAME)
    episode = show.get_episode("1999", "09.04.1999")
    assert episode is not None


def test_get_more_loaded_season():
    """ Aparently not necessary but if this fails it means they added pagination to single seasons """
    show = get_show(SHOW_NAME)
    episode = show.get_episode("2016", "08.01.2016")
    assert episode is not None
    assert episode.episode_number == "08.01.2016"


def test_finding_next_previous():
    show = get_show(SHOW_NAME)
    episode = show.get_episode("2020", "06.11.2020")
    preceding = show.get_preceding_episode(episode)
    following = show.get_following_episode(episode)

    assert preceding.prf_id == "MUHH43002920"
    assert following.prf_id == "MUHH43003120"

    last_season_two = show.get_episode("2011", "16.12.2011")
    following = show.get_following_episode(last_season_two)
    preceding = show.get_preceding_episode(following)

    assert following.prf_id == "MUHH40000112"
    assert preceding.prf_id == last_season_two.prf_id


def test_finding_season_title():
    show = get_show(SHOW_NAME)
    season_title = show.get_season_title("2020")
    assert season_title == "2020"
