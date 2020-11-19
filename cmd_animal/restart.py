import os


def restart(wiki_id):
    os.system(f'docker-compose restart {wiki_id}')
