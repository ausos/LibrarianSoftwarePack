# Librarian software pack
A set of CLI utilities for working with library.

Supported book formats : fb2, fb2.zip, fb2.gz

### Getting Started
`$ pip3 install -r requirements.txt`
##### If you have problems with installation requirements on macOS Catalina try to fix them with commands:
`export LDFLAGS="-L/usr/local/opt/openssl/lib"`

`export CPPFLAGS="-I/usr/local/opt/openssl/include"`
#### Create database with Docker
`sudo docker-compose up -d`

### Working with utils
#### digger.py
```
This is an utility for adding books to database
usage: digger.py [-s] [-a] [-u]
optional arguments:
  -h, --help  show this help message
  -s S        path to directory with books
  -a A        path to the specific book
  -u          updating information about the book in the database
```
Usage example: `python3 digger.py -s /mybooks`
#### seeker.py
```
This is an utility for searching book by author, title, year
usage: seeker.py [-h] [-a A] [-n N] [-y Y] [-s]
optional arguments:
  -h, --help  show this help message
  -a A        author name
  -n N        book name
  -y Y        year
  -s          output only unique identifier of the book
```
Usage example: `python3 seeker.py -a Pushkin`
#### wiper.py

```usage: wiper.py [-h] [-n N] [-a]

This is an utility for deleting book or clear whole library

optional arguments:
  -h, --help  show this help message
  -n N        book number
  -a          delete all books 
```
Usage example: `python3 wiper.py -n 22`

