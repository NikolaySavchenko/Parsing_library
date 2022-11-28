from utils import get_file


def main():
    url = 'https://tululu.org/txt.php?id=32168'
    get_file(url, 'sends_of_mars.txt')


if __name__ == '__main__':
    main()
