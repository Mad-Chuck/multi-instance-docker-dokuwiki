import os


def stop(wiki_id):
    os.system(f'docker-compose stop {wiki_id}')