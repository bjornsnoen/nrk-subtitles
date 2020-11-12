from skam.scraper.episode.sequential import SequentialEpisode

def test_can_fetch_subs():
    conf = {
        "prfId": "MSUB19120116",
        "sequenceNumber": 1,
        "image": [
            {
                "url": "https://gfx.nrk.no/ulFbsZ9nwgSVnAcwaVknDQHVHxggnNh2pjCMHxSRDzhg"
            }
        ],
        "titles": {
            "title": "1. episode",
            "subtitle": "- Du ser ut som en slut."
        },
        "productionYear": 2015,
        "availability": {
            "status": "available"
        }
    }

    episode = SequentialEpisode(conf)
    subs = episode.get_subs()
    assert len(subs) > 0