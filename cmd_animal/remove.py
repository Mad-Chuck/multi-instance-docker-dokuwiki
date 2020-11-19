# ----------------------------------------------- MAIN BODY ------------------------------------------------------------
def dokuwiki_create(params):
    """
    copy default wiki and save it on given name
    use default engine, if other engine check if it exist

    :param params:

    :return:
    """
    log = create_logger('dokuwiki_create')
    doku_name = params.name
    version = params.engine

    # Read engine version
    if version is None:
        try:
            with open('../core_engines/default_version.yml', 'r') as version_file:
                version = yaml.safe_load(version_file)['version']
            version_file.close()
        except FileNotFoundError as e:
            log.error('"./core_engines/default_version.yml" not found. FileNotFoundError: {0}'.format(e))
            raise
        except KeyError as e:
            log.error('Version not found. KeyError: {0}'.format(e))
            raise

    # Read docker compose
    try:
        with open('../docker-compose.yml', 'r') as config_file:
            config = yaml.safe_load(config_file)
        config_file.close()
    except FileNotFoundError as e:
        log.error('"docker-compose.yml" not found. FileNotFoundError: {0}'.format(e))
        raise

    # Read all services names
    try:
        services = config['services']
        services_names = [name for name, conf in services.items()]
        log.info('Read: {0} names'.format(services_names))
    except KeyError as e:
        log.error('services not found in docker-compose.yml. KeyError: {0}'.format(e))
        raise

    # Check is service name free to use
    if doku_name in services_names:
        log.error('Service with given name is already created. '
                  'Change service name or use doku_update.py to modify given service')
        raise

    # define new service
    services[doku_name] = {}
    services[doku_name]['image'] = 'php:7.2-apache'
    services[doku_name]['container_name'] = doku_name

    # add labels
    labels = [
        "traefik.enable=true",
        "traefik.http.routers.{0}.rule=Host(`{0}.localhost`)".format(doku_name),
        "traefik.http.routers.{0}.entrypoints=web".format(doku_name),
    ]
    services[doku_name]['labels'] = labels

    # add volumes
    copy_tree('./core_engines/{0}/conf'.format(version), './wikis_data/{0}/conf'.format(doku_name))
    copy_tree('./core_engines/{0}/data'.format(version), './wikis_data/{0}/data'.format(doku_name))

    volumes = [
        f'./core_engines/{version}/var/www/html:ro',
        f'./wikis_data/{doku_name}/conf:/var/www/html/conf:rw',
        f'./wikis_data/{doku_name}/data:/var/www/html/data:rw',
    ]
    services[doku_name]['volumes'] = volumes

    try:
        with open('../docker-compose.yml', 'w') as config_file:
            yaml.safe_dump(config, config_file, default_flow_style=False)
        config_file.close()
    except FileNotFoundError as e:
        log.error("FileNotFoundError: ", e)
        raise

    os.system(f'docker-compose up -d {doku_name}')