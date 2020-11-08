from skam.scraper.show import Show

def test_can_fetch_skam():
    show = Show("skam")
    episode = show.get_episode(1, 0)
    subs = show.get_subs_for_episode(1, 0)
    assert subs.__len__() > 0
