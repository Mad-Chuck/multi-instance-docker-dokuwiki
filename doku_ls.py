import argparse
import yaml
import logging
import os


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
    log = create_logger('dokuwiki_info')

    # Read docker compose
    try:
        with open('docker-compose.yml', 'r') as config_file:
            config = yaml.safe_load(config_file)
        config_file.close()
    except FileNotFoundError as e:
        log.error('"docker-compose.yml" not found. FileNotFoundError: {0}'.format(e))
        raise

    # Print all possible engines
    try:
        log.info('All engines:')
        for dir in os.listdir('./core_engines'):
            if os.path.isdir(f'./core_engines/{dir}'):
                log.info(f'- {dir}')
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


# ----------------------------------------------- PARAMETERS -----------------------------------------------------------
if __name__ == '__main__':
    # params to set in console script
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    params = parser.parse_args()
    dokuwiki_create(params)
