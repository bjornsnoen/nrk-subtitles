""" Episode class module """
from dataclasses import dataclass


@dataclass
class Episode:
    """ Episode class """

    type: str
    prf_id: str
    title: str
    subtitle: str
    episode_number: int = None
    production_year: int = 2020
    image_url: str = None
