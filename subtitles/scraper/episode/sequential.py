""" Class for shows that follow normal season/episode-in-season structure """
from .episode import Episode


class SequentialEpisode(Episode):
    """ Episode of a sequential type episode """

    def __init__(self, config: dict):
        self.prf_id: str = config["prfId"]
        self.episode_number: int = config["sequenceNumber"]
        self.image_url: str = config["image"][0]["url"]
        self.title: str = config["titles"]["title"]
        self.subtitle: str = config["titles"]["subtitle"]
        self.production_year: int = config["productionYear"]
        self.available = config["availability"]["status"] == "available"
