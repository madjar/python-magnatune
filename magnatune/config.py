import os


config_dir = os.path.expanduser('~/.python-magnatune/')


def check_config_dir():
    """Creates the config dir is needed."""
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
