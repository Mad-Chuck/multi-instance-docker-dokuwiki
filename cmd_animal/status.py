import os


def status(name: str):
    """
    Print status of service

    :param name: service name
    """
    os.system(f'docker-compose ps {name}')
