import argparse
import yaml
import logging


# ------------------------------------------------- CONSTS -------------------------------------------------------------
DEFAULT_ENGINE = 'engine1'

# ---------------------------------------- ADDITIONAL FUNCTIONS --------------------------------------------------------
def create_logger(name):
    """
    create logger fo script
    :param name: name of logger
    :return: logger
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
    formatter = logging.Formatter(log_format)

    ch = logging.StreamHandler()  # console handler
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel('INFO')
    logger.addHandler(ch)
    return logger

# ----------------------------------------------- MAIN BODY ------------------------------------------------------------
def dokuwiki_create(params):
    """
    copy default wiki and save it on given name
    use default engine, if other engine check if it exist

    :param params:
    :return:
    """
    log = create_logger('dokuwiki_create')

    # Read docker compose
    try:
        with open('docker-compose.yml', 'r') as config_file:
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
    if params.name in services_names:
        log.error('Service with given name is already created. '
                  'Change service name or use doku_update.py to modify given service')
        raise

    # define new service
    services[params.name] = {}
    services[params.name]['image'] = 'bitnami/dokuwiki'
    services[params.name]['container_name'] = 'simple-service'

    # add labels
    labels = [
        "traefik.enable=true",
        "traefik.http.routers.{0}.rule=Host(`{0}.localhost)".format(params.name),
        "traefik.http.routers.{0}.entrypoints=web".format(params.name),
    ]
    services[params.name]['labels'] = labels

    # todo: create/copy default wikis data and add to volumes
    volumes = [
        'engine1/inc:/inc:/opt/bitnami/dokuwiki/inc'.format(params.engine),
        'engine1/lib:/bitnami/dokuwiki/lib'.format(params.engine),
        '{0}/conf:/bitnami/dokuwiki/conf'.format(params.name),
        '{0}/data:/bitnami/dokuwiki/data'.format(params.name),
    ]
    services[params.name]['volumes'] = volumes

    try:
        with open('docker-compose.yml', 'w') as config_file:
            yaml.safe_dump(config, config_file, default_flow_style=False)
        config_file.close()
    except FileNotFoundError as e:
        log.error("FileNotFoundError: ", e)
        raise

# ----------------------------------------------- PARAMETERS -----------------------------------------------------------
if __name__ == '__main__':
    # params to set in console script
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--name', type=str, required=True,
                        help='Domain name of dokuwiki')
    parser.add_argument('--engine', type=str, default=DEFAULT_ENGINE,
                        help='Define engine to run dokuwiki, by default its newest.')

    params = parser.parse_args()
    dokuwiki_create(params)
