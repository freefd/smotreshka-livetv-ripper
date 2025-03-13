#!/usr/bin/env python3
""" Smotreshka LiveTV Ripper: Smotreshka Module """

import json
import sys
import random
from datetime import datetime
import requests
from logger_module import Logger

class Smotreshka:
    """ Class to handle initial Smotreshka M3U and EPG data """

    def __init__(self, username: str=None, password: str=None,
                    limit: int=0, mode: str='all', loglevel: int=20) -> None:

        self._lgr = Logger(loglevel=loglevel, classname=self.__class__.__name__)
        self._channels = {}
        self._channels_limit = limit
        self._session = requests.Session()
        self._base_url = 'https://fe.smotreshka.tv'
        self._user_agent = random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTM'
            'L, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33'
        ])

        if username is not None:
            self._smotreshka_username = username
        else:
            self._lgr.logger.critical('Smotreshka user name must be set')

            # sysexits.h: EX_DATAERR
            sys.exit(65)

        if password is not None:
            self._smotreshka_password = password
        else:
            self._lgr.logger.critical('Smotreshka password must be set')

            # sysexits.h: EX_DATAERR
            sys.exit(65)

        self._login()
        self._collect_channels()

        if mode in ('all', 'epg'):
            self._collect_epg()
        if mode in ('all', 'm3u'):
            self._collect_streams()

    def __str__(self) -> str:
        """ Human readable print of the current class """

        return json.dumps(self._channels, ensure_ascii=False, indent=4)

    def _http_request(self, method: str=None, url: str=None,
                        headers: dict=None, data: dict=None) -> dict:
        """ Request endpoint using REST """

        self._lgr.logger.debug('Request %s %s Params=%s', method, url, data)

        try:
            response = self._session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                timeout=60
            )
            return response

        except requests.exceptions.HTTPError as errh:
            self._lgr.logger.critical(
                'Failed to get response from %s. HTTP error %s', url, errh)

            # sysexits.h: EX_DATAERR
            sys.exit(65)

        except requests.exceptions.ConnectionError as errc:
            self._lgr.logger.critical(
                'Failed to get response from %s. Connection error %s', url, errc
                )

            # sysexits.h: EX_UNAVAILABLE
            sys.exit(69)

        except requests.exceptions.Timeout as errt:
            self._lgr.logger.critical(
                'Failed to get response from %s. Timeout error %s', url, errt)

            # sysexits.h: EX_UNAVAILABLE
            sys.exit(69)

        except requests.exceptions.RequestException as errg:
            self._lgr.logger.exception(
                'Failed to get response from %s. Error %s', url, errg)

            # sysexits.h: EX_OSERR
            sys.exit(71)

        return None

    def _login(self) -> None:
        """ Login to Smotreshka """

        self._lgr.logger.info(
            'Login as user %s', self._smotreshka_username)

        response_login = self._http_request(
                method='POST',
                url=f'{self._base_url}/login',
                headers={'User-Agent': self._user_agent},
                data={
                    'email': self._smotreshka_username,
                    'password': self._smotreshka_password,
                }
            )

        if (response_login is None
            or response_login.status_code != requests.codes.ok): # pylint: disable=no-member
            self._lgr.logger.critical(
                'Cannot authenticate: %s', response_login.status_code)

            # sysexits.h: EX_OSERR
            sys.exit(71)

        else:
            self._lgr.logger.info(
                'Authenticated as user %s', self._smotreshka_username)

            self._lgr.logger.debug('Collected cookies %s',
                            requests.utils.dict_from_cookiejar(
                                self._session.cookies)
                            )

    def _collect_channels(self) -> None:
        """ Collect purchased LiveTV channels """

        self._lgr.logger.info('Collect purchased LiveTV channels')

        response_channels = self._http_request(
                method='GET',
                url=f'{self._base_url}/channels',
                headers={
                    'User-Agent': self._user_agent,
                    'Accept': 'application/json'
                }
        )

        if (response_channels is None
            or response_channels.status_code != requests.codes.ok): # pylint: disable=no-member

            self._lgr.logger.critical('Cannot collect LiveTV channels: %s',
                response_channels.status_code)

            # sysexits.h: EX_OSERR
            sys.exit(71)

        else:
            channels_limit = 1
            response_channels_json = response_channels.json()

            if ('channels' in response_channels_json
                and len(response_channels_json.get('channels')) > 0):

                for channel in response_channels_json.get('channels'):
                    if channel.get('info').get(
                                        'purchaseInfo').get('bought') is True:

                        channel_id = channel.get('id')
                        channel_groups = channel.get('info').get(
                                                    'metaInfo').get('genres')
                        channel_number, channel_title = \
                            channel.get('info').get(
                                            'metaInfo').get('title').split('_')
                        channel_logo = \
                            channel.get('info').get(
                                            'mediaInfo').get('thumbnails')[
                                0].get('url')

                        self._lgr.logger.info('Add channel `%s`', channel_title)

                        self._channels[channel_id] = {
                            'number': int(channel_number),
                            'title': channel_title,
                            'groups': channel_groups,
                            'logo': channel_logo,
                            'language': 'ru_RU' # default language
                        }

                    if (self._channels_limit > 0
                        and channels_limit >= self._channels_limit):
                        break
                    channels_limit += 1

                if len(self._channels) < 1:
                    self._lgr.logger.critical(
                    'Did not collect at least one purchased LiveTV channel')

                    # sysexits.h: EX_DATAERR
                    sys.exit(65)
            else:
                self._lgr.logger.critical('List of LiveTV channels is empty')

                # sysexits.h: EX_DATAERR
                sys.exit(65)

    def _collect_streams(self) -> None:
        """ Enrich LiveTV channels with media streams """

        for channel_id, channel_data in self._channels.items():
            self._lgr.logger.info('Collect LiveTV stream `%s` (%s)',
                channel_id,
                channel_data['title'])

            response_channel = self._http_request(
                    method='GET',
                    url=f'{self._base_url}/playback-info/'
                            f'{channel_id}',
                    headers={
                        'User-Agent': self._user_agent,
                        'Accept': 'application/json'
                    }
                )
            if (response_channel is None
                or response_channel.status_code != requests.codes.ok): # pylint: disable=no-member

                self._lgr.logger.warning('Cannot collect LiveTV streams for '
                        'channel `%s` (%s): error %s',
                        channel_id,
                        channel_data['title'],
                        response_channel.status_code
                        )
            else:
                response_channel_json = response_channel.json()

                if ('languages' in response_channel_json
                    and len(response_channel_json.get('languages')) > 0):

                    for language in response_channel_json.get('languages'):

                        if language.get('default'):

                            channel_lang = language.get('id').replace('-', '_')

                            self._lgr.logger.info(
                                'Add language %s to channel `%s` (%s)',
                                channel_lang,
                                channel_id,
                                channel_data['title'])

                            channel_data['language'] = channel_lang

                            if len(language.get('renditions')) > 0:
                                for rendition in language.get('renditions'):

                                    if (rendition.get('default')
                                        and rendition.get('id') == 'Auto'):

                                        self._lgr.logger.info(
                                            'Add LiveTV stream URL to ' \
                                            'channel `%s` (%s)',
                                            channel_id,
                                            channel_data['title'])

                                        channel_data['url']=rendition.get('url')
                                    else:

                                        self._lgr.logger.warning(
                                            'Cannot collect default LiveTV'
                                            'rendition for channel `%s` (%s)',
                                            channel_id,
                                            channel_data['title'])

                                        self._lgr.logger.info(
                                            'Add first found LiveTV stream '
                                            'URL to channel `%s` (%s)',
                                            channel_id,
                                            channel_data['title'])

                                        channel_data['url']=language.get(
                                                    'renditions')[0].get('url')

                                    break
                            else:
                                self._lgr.logger.warning(
                                    'Cannot collect renditions for channel '
                                    '`%s` (%s)',
                                    channel_id,
                                    channel_data['title'])
                        else:

                            channel_lang = language.get('id').replace('-', '_')

                            self._lgr.logger.info(
                                'Add language %s to channel `%s` (%s)',
                                channel_lang,
                                channel_id,
                                channel_data['title'])

                            channel_data['language'] = channel_lang

                            self._lgr.logger.warning(
                                'Cannot collect default LiveTV '
                                'rendition for channel `%s` (%s)',
                                channel_id,
                                channel_data['title'])
                            self._lgr.logger.info(
                                'Add first found LiveTV stream '
                                'URL to channel `%s` (%s)',
                                channel_id,
                                channel_data['title'])

                            channel_data['url']=language.get(
                                        'renditions')[0].get('url')
                        break

                else:
                    self._lgr.logger.warning(
                        'Did not find languages for channel `%s` (%s)',
                        channel_id,
                        channel_data['title'])

    def _collect_epg(self) -> None:
        """ Collect EPG programs for EPG channels """

        for channel_id, channel_data in self._channels.items():

            self._lgr.logger.info('Collect EPG for channel `%s` (%s)',
                channel_id,
                channel_data['title'])

            response_channel_epg = self._http_request(
                    method='GET',
                    url=f'{self._base_url}/channels/'
                            f'{channel_id}/programs',
                    headers={
                        'User-Agent': self._user_agent,
                        'Accept': 'application/json'
                    }
                )

            if (response_channel_epg is None
                or response_channel_epg.status_code != requests.codes.ok): # pylint: disable=no-member

                self._lgr.logger.warning(
                    'Cannot collect EPG for channel `%s` (%s): error %s',
                    channel_id,
                    channel_data['title'],
                    response_channel_epg.status_code
                    )
            else:
                response_channel_epg_json = response_channel_epg.json()

                if (response_channel_epg_json.get('programs')
                    and len(response_channel_epg_json.get('programs')) > 0):

                    channel_data['program'] = []

                    self._lgr.logger.info(
                        'Add EPG programs to channel `%s` (%s)',
                        channel_id,
                        channel_data['title'])

                    for program in response_channel_epg_json.get('programs'):
                        start = program.get('scheduleInfo').get('start')
                        stop = program.get('scheduleInfo').get('end')
                        ptitle = program.get('metaInfo').get('title')
                        desc = program.get('metaInfo').get('description')
                        icon = program.get('mediaInfo').get(
                                                    'thumbnails')[0].get('url')

                        self._lgr.logger.debug(
                            'Add EPG program to channel `%s` (%s): %s (%s-%s)',
                            channel_id,
                            channel_data['title'],
                            ptitle,
                            datetime.fromtimestamp(start).astimezone(
                                ).strftime('%Y-%m-%d %H:%M:%S %z'),
                            datetime.fromtimestamp(stop).astimezone(
                                ).strftime('%Y-%m-%d %H:%M:%S %z'),
                        )

                        channel_data['program'].append(
                                {
                                    'start': start,
                                    'stop': stop,
                                    'title': ptitle,
                                    'desc': desc,
                                    'icon': icon
                                }
                            )
                else:
                    self._lgr.logger.warning(
                        'List of EPG programs is empty for channel `%s` (%s)',
                        channel_id,
                        channel_data['title'])

    def get_channels(self):
        """ Return EPG channels list """

        return self._channels

if __name__ == '__main__':

    Logger().logger.critical(
        'This module must not be run as a standalone application')

    # sysexits.h: EX_OSERR
    sys.exit(71)
