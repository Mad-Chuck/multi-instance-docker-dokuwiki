import os


def stop(wiki_id):
    os.system(f'docker-compose restart {wiki_id}')
