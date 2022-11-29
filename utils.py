import requests
from pathlib import Path


def check_for_redirect(url, response_url):
    if url==response_url:
        return True
    else:
        return False


def get_file(url, file_name, payload=None, folder_name='library'):
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    if check_for_redirect(url, response.url):
        with open(Path(f'{folder_name}/{file_name}'), 'wb') as file:
            file.write(response.content)
