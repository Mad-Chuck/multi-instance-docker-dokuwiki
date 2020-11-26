import os


def run(name: str):
    """
    Start running service

    :param name: service name to run
    """
    os.system(f'docker-compose up -d {name}')
