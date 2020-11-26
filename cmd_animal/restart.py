import os


def restart(name: str):
    """
    Reboot service: Work in progress (currently not working as you may want it to)

    :param name: service name to restart
    """
    os.system(f'docker-compose restart {name}')
