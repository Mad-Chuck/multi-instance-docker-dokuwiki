import yaml
from cmd_animal._logger import _create_logger


def update(name: str):
    """
    Update service to newest version

    :param name: service name to update
    """
    log = _create_logger('animal_update')

    # Read version
    try:
        with open('./core_engines/default_version.yml', 'r') as version_file:
            version = yaml.safe_load(version_file)['version']
            log.info(f'Updating to version: {version}')
        version_file.close()
    except FileNotFoundError as e:
        log.error('"./core_engines/default_version.yml" not found. FileNotFoundError: {0}'.format(e))
        raise
    except KeyError as e:
        log.error('Version not found. KeyError: {0}'.format(e))
        raise

    # Read docker compose
    try:
        with open('./docker-compose.yml', 'r') as config_file:
            config = yaml.safe_load(config_file)
        config_file.close()
    except FileNotFoundError as e:
        log.error('"docker-compose.yml" not found. FileNotFoundError: {0}'.format(e))
        raise

    # Read all services names
    try:
        services = config['services']
        services_names = [name for name, conf in services.items()]
    except KeyError as e:
        log.error('services not found in docker-compose.yml. KeyError: {0}'.format(e))
        raise

    # Check is service name free to use
    if name not in services_names:
        log.error('Service not exist.')
        exit(1)

    # Check current version of engine
    if services[name]['environment']['engine_version'] == version:
        log.info(f'Service is up to date.')
        exit(1)

    log.info(f'Actual service version: { services[name]["environment"]["engine_version"] }')
    services[name]['environment']['engine_version'] = version

    volumes = [
        f'./core_engines/{version}/var/www/html:ro',
        f'./wikis_data/{name}/conf:/var/www/html/conf:rw',
        f'./wikis_data/{name}/data:/var/www/html/data:rw',
    ]
    services[name]['volumes'] = volumes

    try:
        with open('./docker-compose.yml', 'w') as config_file:
            yaml.safe_dump(config, config_file, default_flow_style=False)
        config_file.close()
    except FileNotFoundError as e:
        log.error("FileNotFoundError: ", e)
        raise

    log.info(f'Updated {name} service to {version} version.')
