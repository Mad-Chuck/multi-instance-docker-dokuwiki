import os


def start(name: str):
    """
    Start service from stop status

    :param name: service name
    """
    os.system(f'docker-compose start {name}')
