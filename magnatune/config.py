import logging
import os
import configparser

logger = logging.getLogger(__name__)

config_dir = os.path.expanduser('~/.python-magnatune/')
config_file = os.path.join(config_dir, 'config.ini')


def check_config_dir():
    """Creates the config dir is needed."""
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)


class ConfigArgs:
    AUTHORIZED_OPTIONS = ('verbose', 'format', 'dlformat', 'login', 'extract')

    def __init__(self, args):
        self.args = args
        self.config = configparser.ConfigParser()
        try:
            self.config.read(config_file)
        except configparser.Error as e:
            logger.warning("Error while reading the config file, ignoring :\n%s", e)

        for option in self.config['default']:
            if option not in ConfigArgs.AUTHORIZED_OPTIONS:
                logger.warning('Option "%s" in config file will be ignore', option)

    def __getattr__(self, item):
        arg = getattr(self.args, item)
        if not arg:
            try:
                if item in ConfigArgs.AUTHORIZED_OPTIONS:
                    arg = self.config['default'][item]
            except KeyError:
                pass
        return arg
