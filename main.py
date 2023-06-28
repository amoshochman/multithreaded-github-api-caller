import logging
import sys
from threading import Thread

import requests
import config

logging.basicConfig(filename=config.LOG_FILE, level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')


def call_git_api(url, results):
    headers = {
        'Authorization': 'Bearer ' + config.TOKEN,
        'Accept': 'application/vnd.github.v3+json'
    }
    response = None
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        logging.error(f"{e} - Query: {url}")
    if not response:
        logging.error(f"API request failed with status code {response.status_code} - Query: {url}")
        logging.error(f"Response body: {response.text}")
        return
    if response.status_code == 200:
        try:
            count = response.json().get('total_count')
            results.append(count)
        except (ValueError, KeyError):
            logging.error(f"No total_count on response - Query: {url}")


def parse_files(path):
    results = []
    threads = []
    try:
        with open(path, encoding='utf-8') as file:
            queries = [query.strip() for query in file]
    except OSError as e:
        logging.error(f"An error occurred while trying to read file '{path}': {str(e)}")
        sys.exit(1)
    for query in queries:
        while config.MAX_THREADS_NUM <= len([thread for thread in threads if thread.is_alive()]):
            pass
        thread = Thread(target=call_git_api, args=(query.strip(), results))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join(timeout=config.TIME_OUT)
        if thread.is_alive():
            logging.error(f"A thread took longer than the specified timeout: {thread}")
    print(results)


if __name__ == '__main__':
    parse_files(config.QUERIES_FILE)
