from utils import get_file


def main():
    url = 'https://tululu.org/txt.php?id=32168'
    url_tululu = 'https://tululu.org/txt.php?id=239'
    for id in range(1, 11):
        url_temp = f'https://tululu.org/txt.php?id={id}'
        get_file(url_temp, f'id{id}.txt')


if __name__ == '__main__':
    main()
