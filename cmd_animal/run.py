import os


def run(wiki_id):
    os.system(f'docker-compose start {wiki_id}')
