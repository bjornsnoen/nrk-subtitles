from subtitles.scraper.show.show import get_show

SHOW_NAME = "skam"


def test_get_season_one():
    show = get_show(SHOW_NAME)
    episodes = show.get_episodes(1)
    assert len(episodes) == 11


def test_get_all_seasons():
    show = get_show(SHOW_NAME)
    seasons = show.get_available_seasons()
    assert len(seasons) == 4


def test_get_first_episode_of_show():
    show = get_show(SHOW_NAME)
    episode = show.get_episode(1, 1)
    assert episode.episode_number == 1


def test_finding_next_previous():
    show = get_show(SHOW_NAME)
    episode = show.get_episode(1, 2)
    preceding = show.get_preceding_episode(episode)
    following = show.get_following_episode(episode)

    assert preceding.prf_id == "MSUB19120116"
    assert following.prf_id == "MSUB19120316"

    last_season_one = show.get_episode(1, 11)
    following = show.get_following_episode(last_season_one)
    preceding = show.get_preceding_episode(following)

    assert following.prf_id == "MYNT15000116"
    assert preceding.prf_id == last_season_one.prf_id
