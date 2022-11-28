import requests
from pathlib import Path


def get_file(url, file_name, payload=None, folder_name='library'):
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(Path(f'{folder_name}/{file_name}'), 'wb') as file:
        file.write(response.content)

