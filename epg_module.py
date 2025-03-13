#!/usr/bin/env python3
""" Smotreshka LiveTV Ripper: EPG Module """

import json
import sys
import html
from dataclasses import dataclass, field, asdict
from datetime import datetime
from logger_module import Logger

@dataclass
class EPGProgramEntry:
    """
    EPG program entity from XMLTV standard

    Attributes
    ----------
    channel_id: str
        Unique identifier to map the program entry to M3U entry and EPG channel
    start: str
        Program start time in unix epoch timestamp
    stop: str
        Program end time in unix epoch timestamp
    title: str
        Title of the program
    desc: str
        Channel order number
    category: list[str]
        List of program categories
    icon: str
        URL to program entry thumbnail
    """

    channel_id: str = None
    start: str = None
    stop: str = None
    title: str = None
    desc: str = None
    category: list[str] = None
    icon: str = None

    def __post_init__(self, loglevel: int=20) -> None:
        """ Post init preparations """

        self._lgr = Logger(loglevel=loglevel, classname=self.__class__.__name__)
        self._validate()

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

        for attr in ('channel_id', 'start', 'stop', 'title', 'desc'):
            if getattr(self, attr) is None:
                self._lgr.logger.critical(
                    '`%s` attribute must be set', attr)

                # sysexits.h: EX_DATAERR
                sys.exit(65)

    def make_dict(self) -> dict:
        """ Return current class as a dict """

        return self.__dict__

@dataclass
class EPGChannelEntry:
    """
    EPG channel entry with programs for XMLTV notation

    Attributes
    ----------
    channel_id: str
        Unique identifier to map the channel to M3U entry 
    display_name: str
        Name of the channel or entry
    icon: str
        URL to network resource with media stream
    language: str
        Language of the EPG channel entry and EPG program entries
    program: list[EPGProgramEntry]
        List of EPG program entries
    """

    channel_id: str = None
    display_name: str = None
    icon: str = None
    language: str = 'ru_RU'
    program: list[EPGProgramEntry] = field(default_factory=list)

    def __post_init__(self, loglevel: int=20) -> None:
        """ Post init preparations """

        self._lgr = Logger(loglevel=loglevel, classname=self.__class__.__name__)
        self._validate()

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

        for attr in ('channel_id', 'display_name', 'icon'):
            if getattr(self, attr) is None:
                self._lgr.logger.critical(
                    '`%s` attribute must be set', attr)

                # sysexits.h: EX_DATAERR
                sys.exit(65)

    def make_dict(self) -> dict:
        """ Return current class as a dict """

        return self.__dict__

    def get_attribute(self, attr: str = None) -> str | None:
        """ Return the attribute if exists """

        if hasattr(self, attr):
            return getattr(self, attr)

        return None

    def make_epg_entry(self) -> str:
        """
        Create EPG record

        TODO: rewrite with XML processor
        """

        return_entry = f'<channel id="{self.channel_id}">\n'
        for key, value in self.__dict__.items():

            if (isinstance(value, int | str)
                and key not in ('channel_id', 'language', 'program')):

                key_normalized = key.replace("_", "-")
                value_escaped = html.escape(value)
                language = self.language

                if key == 'icon':
                    return_entry+=f'<{key_normalized} src="{value_escaped}"/>\n'
                else:
                    return_entry+=f'<{key_normalized} lang="{language}">' \
                                    f'{value_escaped}</{key_normalized}>\n'

        return_entry += '</channel>\n'

        for program in self.program:
            start = datetime.fromtimestamp(
                    program['start']).astimezone().strftime('%Y%m%d%H%M%S %z')
            stop = datetime.fromtimestamp(
                    program['stop']).astimezone().strftime('%Y%m%d%H%M%S %z')
            channel_id = program['channel_id']
            title = html.escape(program['title'])
            desc = html.escape(program['desc'])
            lang = self.language
            icon = program['icon']

            return_entry += f'<programme start="{start}" ' \
                            f'stop="{stop}" ' \
                            f'channel="{channel_id}">\n' \
                            f'<title lang="{lang}">{title}</title>\n' \
                            f'<desc lang="{lang}">{desc}</desc>\n' \
                            f'<icon src="{icon}"/>\n'

            return_entry += '\n'.join(map(
                lambda cat: f'<category lang="{lang}">{cat}</category>',
                                                        program['category']))
            return_entry += '\n</programme>\n'

        self._lgr.logger.debug(
            'Generate XMLTV entry for channel `%s`', self.display_name)

        return return_entry

class EPGListing:
    """ Class to generate XMLTV listing from EPG channel and program entries """

    def __init__(self,
                generator_name: str = 'dummy',
                generator_url: str = 'https://localhost',
                loglevel: int=20):

        self._lgr = Logger(loglevel=loglevel, classname=self.__class__.__name__)
        self._epg_channels: list[EPGChannelEntry] = []
        self._generator_name: str = generator_name
        self._generator_url: str = generator_url

    def __str__(self) -> str:
        """ Human readable print of the current class """

        return json.dumps(
            [ch.make_dict() for ch in self._epg_channels],
            ensure_ascii=False, indent=4
        )

    def append_epg_channel(self, channel: EPGChannelEntry) -> None:
        """ Append EPG channel entry to existing list """

        self._epg_channels.append(channel)
        self._lgr.logger.info('Add EPG channel `%s`', channel.display_name)
        self._lgr.logger.debug('%s', channel)

    def append_epg_program(self,
                    channel: EPGChannelEntry,
                    program: EPGProgramEntry) -> None:
        """ Append EPG program entry to existing EPG channel """

        for chnl in self._epg_channels:
            if channel.get_attribute('channel_id') == chnl.channel_id:
                channel.program.append(asdict(program))

    def make_epg_listing(self) -> dict:
        """
        Create EPG listing

        TODO: rewrite with XML processor
        """

        date_gen = datetime.now().astimezone().strftime('%Y%m%d%H%M%S %z')
        return_listing = ('<?xml version="1.0" encoding="utf-8" ?>\n'
            '<!DOCTYPE tv SYSTEM "https://raw.githubusercontent.com/XMLTV/xmltv'
            '/refs/heads/master/xmltv.dtd">\n'
            f'<tv date="{date_gen}" '
            f'generator-info-name="{self._generator_name}" '
            f'generator-info-url="{self._generator_url}">\n')

        for channel in self._epg_channels:
            return_listing += channel.make_epg_entry()

        return_listing += '</tv>'

        return return_listing

if __name__ == '__main__':

    Logger().logger.critical(
        'This module must not be run as a standalone application')

    # sysexits.h: EX_OSERR
    sys.exit(71)
