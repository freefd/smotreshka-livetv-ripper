#!/usr/bin/env python3
""" Smotreshka LiveTV Ripper: M3U Module """

import json
import sys
from dataclasses import dataclass
from logger_module import Logger

@dataclass
class M3UChannelEntry:
    """
    M3U record entry of M3U Plus notation

    Attributes
    ----------
    duration: str
        Duration of the channel or entry as a string formatted as a float or
        as an integer (with or without sign), is set to infinite as static value
    title: str
        Name of the channel or entry (the part after the last colon in an
        #EXTINF row)
    url: str
        URL to network resource with media stream
    group_title: str
        Semicolon separated list of channel categories
    tvg_chno: str
        Channel order number
    tvg_id: str
        Unique identifier to map the channel to Electronic Program Guide
    tvg_log: str
        URL to channel logo
    """

    duration: int = -1
    title: str = None
    url: str = None
    group_title: str = None
    tvg_chno: str = None
    tvg_id: str = None
    tvg_logo: str = None
    tvg_language: str = 'ru_RU'

    def __post_init__(self, loglevel: int=20) -> None:
        """ Post init preparations """

        self._lgr = Logger(loglevel=loglevel, classname=self.__class__.__name__)
        self._validate()
        self._update_group_title()

    def __str__(self) -> str:
        """ Human readable print of the current class """

        return_obj = {}

        for key, value in self.__dict__.items():
            return_obj[key] = {
                'value': value,
                'type': type(value).__name__
            }

        return json.dumps(return_obj, ensure_ascii=False, indent=4)

    def _validate(self) -> None:
        """ Validate the required attributes are populated """

        for attr in ('tvg_id', 'url', 'title'):
            if getattr(self, attr) is None:
                self._lgr.logger.critical('`%s` attribute must be set', attr)

                # sysexits.h: EX_DATAERR
                sys.exit(65)

    def _update_group_title(self) -> None:
        """ Convert group_title list attribute to a string """

        if self.group_title is not None:
            self.group_title = ';'.join(self.group_title)

    def make_dict(self) -> dict:
        """ Return current class as a dict """

        return self.__dict__

    def make_m3u_entry(self) -> str:
        """ Create M3U record """

        return_entry = f'#EXTINF:{self.duration}'
        for key, value in self.__dict__.items():
            if (isinstance(value, int | str)
                and key not in ('duration', 'title', 'url')):
                return_entry += f' {key.replace("_", "-")}="{value}"'

        self._lgr.logger.debug(
            'Generate M3U entry for channel `%s`', self.title)

        return f'{return_entry}, {self.title}\n{self.url}\n'

class M3UPlaylist:
    """ Class to generate M3U playlist from M3U channel entries """

    def __init__(self, loglevel: int=20) -> None:
        self._lgr = Logger(loglevel=loglevel, classname=self.__class__.__name__)
        self._m3u_channels: list[M3UChannelEntry] = []

    def __str__(self) -> str:
        """ Human readable print of the current class """

        return json.dumps(
            [ch.make_dict() for ch in self._m3u_channels],
            ensure_ascii=False, indent=4
        )

    def append_m3u_channel(self, channel: M3UChannelEntry) -> None:
        """ Append M3U channel entry to existing playlist """

        self._m3u_channels.append(channel)
        self._lgr.logger.info('Add M3U channel `%s`', channel.title)
        self._lgr.logger.debug('%s', channel)

    def make_m3u_playlist(self) -> dict:
        """ Create M3U playlist """

        self._lgr.logger.debug('Generate M3U playlist')

        return_playlist = '#EXTM3U\n'
        for channel in self._m3u_channels:
            return_playlist += channel.make_m3u_entry()

        return return_playlist

if __name__ == '__main__':

    Logger().logger.critical(
        'This module must not be run as a standalone application')

    # sysexits.h: EX_OSERR
    sys.exit(71)
