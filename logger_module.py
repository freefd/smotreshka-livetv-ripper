#!/usr/bin/env python3
""" Smotreshka LiveTV Ripper: Logger Module """

import re
import sys
import logging

class SensitiveDataFormatter(logging.Formatter):
    """ Logging Sensitive Data Formatter """

    @staticmethod
    def _filter(message: str=None):
        filters = [
            [r"'password': '.+?'", "'password': '*****'"],
            [r'password=.+?', 'password=*****']
        ]
        for filter_pattern in filters:
            message = re.sub(filter_pattern[0], filter_pattern[1], message)
        return message

    def format(self, record: str=''):
        original = logging.Formatter.format(self, record)
        return self._filter(original)

class Logger:
    """ Logger class """

    def __init__(self, loglevel: int = 20, classname: str=None):
        self.logger = logging.getLogger(classname)
        self._console_handler = logging.StreamHandler(sys.stdout)
        self._console_handler.setFormatter(
            SensitiveDataFormatter(
                '[%(asctime)s] %(levelname)s %(module)s.py::'
                '%(name)s::%(funcName)s(): %(message)s',
            )
        )
        self.logger.addHandler(self._console_handler)
        self.logger.setLevel(loglevel)

if __name__ == '__main__':

    Logger().logger.critical(
        'This module must not be run as a standalone application')

    # sysexits.h: EX_OSERR
    sys.exit(71)
