import os
import yaml
from cmd_animal._logger import _create_logger
from distutils.dir_util import copy_tree


def create(name: str, engine: str = 'default'):
    """
    Create wiki with separated data, running on given engine.

    :param name: service name to create
    :param engine: if given engine does not exist - use default version.
    """

    log = _create_logger('animal_create')
    doku_name = name
    version = engine

    # Read engine version
    if version == 'default' or version not in os.listdir('./core_engines'):
        try:
            with open('./core_engines/default_version.yml', 'r') as version_file:
                version = yaml.safe_load(version_file)['version']
                log.info('Used default version engine')
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
        log.info(f'Services in config: {services_names}')
    except KeyError as e:
        log.error('services not found in docker-compose.yml. KeyError: {0}'.format(e))
        raise

    # Check is service name free to use
    if doku_name in services_names:
        log.error('Service with given name is already created. '
                  'Change service name or use update to update given service')
        exit(1)

    # define new service
    services[doku_name] = {}
    services[doku_name]['build'] = '.'
    services[doku_name]['container_name'] = doku_name
    services[doku_name]['environment'] = {}
    services[doku_name]['environment']['engine_version'] = version

    # add labels
    labels = [
        "traefik.enable=true",
        "traefik.http.routers.{0}.rule=Host(`{0}.localhost`)".format(doku_name),
        "traefik.http.routers.{0}.entrypoints=web".format(doku_name),
    ]
    services[doku_name]['labels'] = labels

    # add volumes
    copy_tree(f'./core_engines/{version}/conf', f'./wikis_data/{doku_name}/conf')
    copy_tree(f'./core_engines/{version}/data', f'./wikis_data/{doku_name}/data')

    volumes = [
        f'./core_engines/{version}:/var/www/html:ro',
        f'./wikis_data/{doku_name}/conf:/var/www/html/conf:rw',
        f'./wikis_data/{doku_name}/data:/var/www/html/data:rw',
    ]
    services[doku_name]['volumes'] = volumes

    try:
        with open('./docker-compose.yml', 'w') as config_file:
            yaml.safe_dump(config, config_file, default_flow_style=False)
        config_file.close()
    except FileNotFoundError as e:
        log.error("FileNotFoundError: ", e)
        raise

    log.info(f'Created {doku_name} service.')
