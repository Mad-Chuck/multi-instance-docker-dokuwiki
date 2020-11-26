import os


def restart(name: str):
    """
    Reboot service

    :param name: service name to restart
    """
    os.system(f'docker-compose restart {name}')
