from scraper import Show

show = Show("skam")
subs = show.get_subs_for_episode(1, 0)
print(subs)