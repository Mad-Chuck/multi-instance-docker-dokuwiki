import os


def start(wiki_id):
    os.system(f'docker-compose start {wiki_id}')
