import os


def stop(wiki_id):
    os.system(f'docker-compose ps {wiki_id}')