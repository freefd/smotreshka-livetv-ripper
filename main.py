#!/usr/bin/env python3
""" Smotreshka LiveTV Ripper """

import argparse
import sys
from pathlib import Path
from logger_module import Logger
from m3u_module import M3UChannelEntry, M3UPlaylist
from epg_module import EPGChannelEntry, EPGProgramEntry, EPGListing
from smotreshka_module import Smotreshka

GENERATOR_VERSION='0.1'
GENERATOR_NAME=f'Smotreshka-Live-TV-Ripper-v{GENERATOR_VERSION}'
GENERATOR_URL='https://github.com/freefd/smotreshka-livetv-ripper'

def get_args() -> dict:
    """ Parse CLI arguments """

    args_parser = argparse.ArgumentParser(
            description='Smotreshka Live TV Ripper')
    args_parser.add_argument(
                '-u', '--username',
                type=str,
                default=None,
                help='User name to login. Default: not set',
                required=True
            )
    args_parser.add_argument(
                '-p', '--password',
                type=str,
                default=None,
                help='Password to login. Default: not set',
                required=True
            )
    args_parser.add_argument(
                '-m3u', '--m3u-output',
                type=str,
                default='smotreshka.m3u',
                help='Generated M3U file path. Default: smotreshka.m3u'
            )
    args_parser.add_argument(
                '-xmltv', '--xmltv-output',
                type=str,
                default='smotreshka.xmltv.xml',
                help='Generated XMLTV file path. Default: smotreshka.xmltv.xml'
            )
    args_parser.add_argument(
                '-l', '--limit',
                type=int,
                default=0,
                help='Limit the number of channels for processing. Default: 0'
            )
    args_parser.add_argument(
                '-m', '--mode',
                type=str,
                help='Generator mode. Default: all',
                choices=['all', 'epg', 'm3u'],
                default='all'
            )
    args_parser.add_argument(
                '-o', '--overwrite',
                help='Allow to overwrite existing output files. Default: false',
                action='store_true',
                default=False
            )

    args_parser.add_argument(
        '--verbose', '-v', help='Enable verbose output. Default: 0',
        required=False, default=0, action='count'
    )

    args_parsed = args_parser.parse_args()
    args_parsed.verbose = 30 - (10 * int(args_parsed.verbose)) if int(
        args_parsed.verbose) > 0 else 20

    args_parsed.verbose = 10 if args_parsed.verbose<=0 else args_parsed.verbose

    return args_parsed

if __name__ == '__main__':

    args = get_args()
    lgr  = Logger(loglevel=args.verbose, classname=__name__)

    if (Path(args.xmltv_output).exists()
        and not args.overwrite
        and args.mode in ('all', 'epg')):
        lgr.logger.critical(
            'Target XMLTV listing file %s already exists', args.xmltv_output)

        # sysexits.h: EX_CANTCREAT
        sys.exit(73)

    if (Path(args.m3u_output).exists()
        and not args.overwrite
        and args.mode in ('all', 'm3u')):
        lgr.logger.critical(
            'Target M3U playlist file %s already exists', args.m3u_output)

        # sysexits.h: EX_CANTCREAT
        sys.exit(73)


    smotreshka_channels = Smotreshka(
                                username=args.username,
                                password=args.password,
                                limit=args.limit,
                                mode=args.mode,
                                loglevel=args.verbose
                            ).get_channels()

    if args.mode in ('all', 'epg'):

        epg_listing_obj = EPGListing(
                generator_name = GENERATOR_NAME,
                generator_url = GENERATOR_URL
            )

        for channel_id, channel_data in smotreshka_channels.items():
            epg_channel = EPGChannelEntry(
                    channel_id=channel_id,
                    display_name=channel_data['title'],
                    icon=channel_data['logo'],
                    language=channel_data['language']
                )

            epg_listing_obj.append_epg_channel(epg_channel)

            if 'program' in channel_data:
                for program in channel_data['program']:
                    epg_channel_program = EPGProgramEntry(
                        channel_id=channel_id,
                        category=channel_data['groups'],
                        start=program['start'],
                        stop=program['stop'],
                        title=program['title'],
                        desc=program['desc'],
                        icon=program['icon']
                    )

                    epg_listing_obj.append_epg_program(
                                            epg_channel, epg_channel_program)

        with open(
            file=args.xmltv_output,
            mode='w',
            encoding='utf8'
        ) as xmltv_listing:
            xmltv_listing.write(epg_listing_obj.make_epg_listing())
            lgr.logger.info(
                'Please find the generated EPG XMLTV listing\n\t- %s',
                Path(args.xmltv_output).resolve())

    if args.mode in ('all', 'm3u'):

        m3u_playlist_obj = M3UPlaylist()

        for channel_id, channel_data in smotreshka_channels.items():
            m3u_playlist_obj.append_m3u_channel(
                M3UChannelEntry(
                    title=channel_data['title'],
                    url=channel_data['url'],
                    group_title=channel_data['groups'],
                    tvg_chno=channel_data['number'],
                    tvg_id=channel_id,
                    tvg_logo=channel_data['logo'],
                    tvg_language=channel_data['language']
                )
            )

        with open(
            file=args.m3u_output,
            mode='w',
            encoding='utf8'
        ) as m3u_playlist:
            m3u_playlist.write(m3u_playlist_obj.make_m3u_playlist())
            lgr.logger.info(
                'Please find generated M3U playlist\n\t- %s',
                Path(args.m3u_output).resolve())
