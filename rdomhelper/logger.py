# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import functools
import io
import logging
import sys
import threading

from dciclient.v1.api import file as dci_file


def setup_logging(dci_context):
    logger = logging.getLogger('__chainsaw__')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s::%(levelname)s::%(message)s")
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('chainsaw.log', mode='w')
    file_handler.setFormatter(formatter)

    dci_handler = DciHandler(dci_context)
    dci_handler.setFormatter(formatter)

    try:
        import colorlog

        colored_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s::%(levelname)s::%(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red'
            }
        )
        stream_handler.setFormatter(colored_formatter)
    except ImportError:
        pass
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.addHandler(dci_handler)


class DciHandler(logging.Handler):
    def __init__(self, dci_context):
        logging.Handler.__init__(self)
        self._dci_context = dci_context
        self._idx_file = 0
        self._current_log = io.StringIO()
        self._threshold_log = 512 * 1024  # 512K
        self._interval = 60  # 1 minute
        timer_handle = functools.partial(self.handle, record=None)
        self._timer = threading.Timer(self._interval, timer_handle)
        try:
            self._timer.start()
        except KeyboardInterrupt:
            self._timer.cancel()
            raise

    def _send_log_file(self):
        if not self._dci_context.last_jobstate_id:
            return
        jobstate_id = self._dci_context.last_jobstate_id
        dci_file.create(self._dci_context, 'chainsaw.log-%s' % self._idx_file,
                        self._current_log.getvalue(), 'text/plain',
                        jobstate_id)
        self._current_log.truncate(0)
        self._current_log.seek(0)
        self._idx_file += 1

    def emit(self, record):
        # run by the timer
        if record is None:
            if len(self._current_log.getvalue()) > 0:
                self._send_log_file()
            return
        msg = u"%s\n" % self.format(record)
        self._current_log.write(msg)
        #  if its an error then send the log
        if record.levelno == logging.ERROR:
            self._send_log_file()
        #  if we reach the current log threshold
        elif len(self._current_log.getvalue()) > self._threshold_log:
            self._send_log_file()
