import os


def status(wiki_id):
    os.system(f'docker-compose ps {wiki_id}')