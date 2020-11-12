""" Class for shows that run continuously, not having an episode 1 and 2 every season """
from .episode import Episode


class StandardEpisode(Episode):
    """ Episode of a sequential type episode """

    def __init__(self, config: dict):
        self.prf_id: str = config["prfId"]
        self.episode_number: int = config["firstTransmissionDateDisplayValue"]
        self.image_url: str = config["image"][0]["url"]
        self.title: str = config["titles"]["title"]
        self.subtitle: str = config["titles"]["subtitle"]
        self.production_year: int = config["productionYear"]
        self.available = config["availability"]["status"] == "available"
