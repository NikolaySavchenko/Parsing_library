# Parsing library

It's connects to [Tululu](https://tululu.org/) library, fetch books and their cover and save it.

## How to install


Python3 should already be installed. Use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### To download books by ID use:

Example for command line:
```
$ python '\parsing_library> python3 main.py start_id end_id 
```

Where `start_id` - book ID on [Tululu](https://tululu.org/) library from which the download will start.

`end_id` - book ID on [Tululu](https://tululu.org/) library where the download ends.

### To download books in the Science Fiction genre only:
```
$ python '\parsing_library> python3 parse_tululu_cathegory.py start_page end_page --dest_folder --skip_imgs --skip_txt --json_path
```
Where `start_page` - book on page [Tululu](https://tululu.org/l55/) library ganres Science Fiction from which the download will start.

`end_page` - book on page [Tululu](https://tululu.org/l55/) library ganres Science Fiction where download ends.

`--dest_folder` - if it's True, you will see book folder path. 

`--skip_imgs ` - if it's True, book cover will NOT be downloaded.

`--skip_txt` - if it's True, book text will NOT be downloaded.

`--json_path` - if it's True, you will see json folder path with the book description.

## Project Goals

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).