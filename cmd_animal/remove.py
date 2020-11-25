import shutil
import yaml
import subprocess
from cmd_animal._logger import _create_logger


def remove(name: str):
    """
    Remove service from list if inactive.

    :param name: service name to remove
    """
    log = _create_logger('animal_remove')

    s = str(subprocess.check_output('docker-compose ps', shell=True), 'utf-8').split()
    if name == 'traefik' or name in s:
        log.error('Cannot remove running service. Try to stop it first.')
        exit(1)

    # Read docker compose
    try:
        with open('./docker-compose.yml', 'r') as config_file:
            config = yaml.safe_load(config_file)
        config_file.close()
    except FileNotFoundError as e:
        log.error(f'"docker-compose.yml" not found. FileNotFoundError: {e}')
        raise

    # Read all services names
    try:
        services = config['services']
        services_names = [name for name, conf in services.items()]
        log.info(f'Read: {services_names} names')
    except KeyError as e:
        log.error(f'services not found in docker-compose.yml. KeyError: {e}')
        raise

    # Check is service name free to use
    if name not in services_names:
        log.error('Service with given name not exist.')
        exit(1)

    del services[name]

    try:
        with open('./docker-compose.yml', 'w') as config_file:
            yaml.safe_dump(config, config_file, default_flow_style=False)
        config_file.close()
    except FileNotFoundError as e:
        log.error(f'FileNotFoundError: {e}')
        raise
    log.info(f'Service {name} removed from config file.')

    shutil.rmtree(f'./wikis_data/{name}')
    log.info(f'Removed {name} data.')
