import os


def stop(name: str):
    """
    Stop service

    :param name: service name
    """
    os.system(f'docker-compose stop {name}')
