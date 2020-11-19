import os
import yaml
from cmd_animal._logger import _create_logger


def ls():
    """
    print all engine and service list
    """

    log = _create_logger('animal_print')

    # Read docker compose
    try:
        with open('./docker-compose.yml', 'r') as config_file:
            config = yaml.safe_load(config_file)
        config_file.close()
    except FileNotFoundError as e:
        log.error('"docker-compose.yml" not found. FileNotFoundError: {0}'.format(e))
        raise

    # Print all possible engines
    try:
        log.info('All engines:')
        for engine_dir in os.listdir('./core_engines'):
            if os.path.isdir(f'./core_engines/{engine_dir}'):
                log.info(f'- {engine_dir}')
    except FileNotFoundError as e:
        log.error('Path not found: {0}'.format(e))
        raise

    # Print  all services configuration
    try:
        services = config['services']
        log.info('Services in use:')
        for name, conf in services.items():
            log.info(f'- {name}')
    except KeyError as e:
        log.error('services not found in docker-compose.yml. KeyError: {0}'.format(e))
        raise
