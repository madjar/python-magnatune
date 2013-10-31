import logging
import os
import configparser
from xdg.BaseDirectory import save_config_path, load_config_paths

logger = logging.getLogger(__name__)

config_dir = save_config_path('python-magnatune')

AUTHORIZED_OPTIONS = {'verbose': False,
                      'quiet': False,
                      'format': 'ogg',
                      'dlformat': 'web',
                      'login': None,
                      'extract': None}


def setdefault_from_config(args):
    config = {}
    for f in load_config_paths('python-magnatune', 'config.ini'):
        logger.debug('Reading form config file: %s', f)
        parser = configparser.ConfigParser()
        try:
            parser.read(f)
            for option, value in parser['magnatune'].items():
                if option not in AUTHORIZED_OPTIONS:
                    logger.warning('Option "%s" in config file %s will be ignored', option, f)
                else:
                    config.setdefault(option, value)
        except configparser.Error as e:
            logger.warning("Error while reading the config file %s, ignoring :\n%s", f, e)

    for k, v in AUTHORIZED_OPTIONS.items():
        config.setdefault(k, v)

    return {key: config.get(key) if value is None else value
            for key, value in vars(args).items()}
