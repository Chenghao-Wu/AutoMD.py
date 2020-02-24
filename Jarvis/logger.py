#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from .conf import LOG, OUT_PATH


def setup_logger(to_file=LOG['TO_FILE']):
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG['ROOT_LEVEL'])
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s','%Y-%m-%d %H:%M:%S')

    if to_file:
        file_handler = logging.FileHandler(os.path.join(OUT_PATH, 'analysis_log.log'), mode='w')
        file_handler.setLevel(LOG['FILE_LEVEL'])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOG['CONSOLE_LEVEL'])
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger