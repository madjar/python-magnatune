import logging
import os
import configparser
from xdg.BaseDirectory import save_config_path

logger = logging.getLogger(__name__)

config_dir = save_config_path('python-magnatune')
# TODO : use load_config_path for the next one
config_file = os.path.join(config_dir, 'config.ini')


class ConfigArgs:
    AUTHORIZED_OPTIONS = {'verbose': False,
                          'quiet': False,
                          'format': 'ogg',
                          'dlformat': 'web',
                          'login': None,
                          'extract': None}

    def __init__(self, args):
        self.args = args
        parser = configparser.ConfigParser()
        try:
            parser.read(config_file)
            self.config = parser['magnatune']
        except configparser.Error as e:
            logger.warning("Error while reading the config file, ignoring :\n%s", e)
            self.config = {}
        except KeyError:
            self.config = {}

        for option in self.config:
            if option not in ConfigArgs.AUTHORIZED_OPTIONS:
                logger.warning('Option "%s" in config file will be ignore', option)

    def __getattr__(self, item):
        arg = getattr(self.args, item)
        if not arg and item in ConfigArgs.AUTHORIZED_OPTIONS:
            arg = self.config.get(item, ConfigArgs.AUTHORIZED_OPTIONS[item])
        return arg
