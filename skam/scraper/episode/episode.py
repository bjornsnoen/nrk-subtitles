""" Shared functionality for episodes in abstract class """
from __future__ import annotations

from abc import ABC
from io import StringIO
from typing import List, Union

import requests
import webvtt


class Episode(ABC):
    """ Abstract class, has logic common to all types of episode """

    prf_id: str
    title: str
    subtitle: str
    image_url: str
    _episode_number: Union[int, str]
    _available: bool

    def get_subs(self) -> List[str]:
        """ Get subs for episode in season, should be removed """
        prf_id = self.prf_id
        prefix = prf_id[0:6]
        cache = prf_id[6:8]
        link = (
            "https://undertekst.nrk.no/prod/{prefix}/{dir}/{prfid}/{LANG}/{prfid}.vtt"
        )
        real_link = link.format(prfid=prf_id, prefix=prefix, dir=cache, LANG="TTV")
        response = requests.get(real_link)
        if response.status_code != 200:
            real_link = link.format(prfid=prf_id, prefix=prefix, dir=cache, LANG="NOR")
            response = requests.get(real_link)
        if response.status_code != 200:
            raise requests.exceptions.InvalidURL
        return self._parse_subs(response.text)

    def _parse_subs(self, subs: str) -> List[str]:
        buffer = StringIO(subs)
        lines = []
        for caption in webvtt.read_buffer(buffer):
            try:
                lines.append(caption.text)
            except:
                pass
        return lines

    @property
    def episode_number(self):
        """ Property """
        return self._episode_number if self._episode_number else self.prf_id

    @episode_number.setter
    def episode_number(self, value: Union[int, str]):
        """ Property """
        self._episode_number = value

    @property
    def available(self) -> bool:
        """ Whether the show is available for streaming or not """
        return self._available

    @available.setter
    def available(self, availability: bool):
        self._available = availability

    def __eq__(self, other: Episode) -> bool:
        if other is None:
            return False
        return self.prf_id == other.prf_id
