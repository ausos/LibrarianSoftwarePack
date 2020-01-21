import argparse
import gzip
import os
import xml.etree.cElementTree as ET
import zipfile

import data_base as db

parser = argparse.ArgumentParser(description='Adding books to database')
parser.add_argument('-s', help='Path to the directory with books')
parser.add_argument('-a', help='Path to the specific book')
parser.add_argument('-u', default=False, action='store_true',
                    help='Updating information about the book in the database')


def book_parser(book_path):
    if book_path.endswith('fb2'):
        for event, elem in ET.iterparse(book_path, events=('end', 'end-ns')):
            if elem and elem.tag.endswith('title-info'):
                root = elem
            elif elem and elem.tag.endswith('publish-info'):
                root_second = elem
                break
    else:
        if book_path.endswith('.zip'):
            book = zipfile.ZipFile(book_path)
            book = book.open(book.namelist()[0])
        elif book_path.endswith('.gz'):
            book = gzip.open(book_path, 'r')

        xml_text = list()
        while True:
            line = book.readline().decode('utf-8')
            xml_text.append(line)
            if '</publish-info>' in line:
                break
        xml_text = ''.join(xml_text)

        parser = ET.XMLPullParser(['start', 'end'])
        parser.feed(xml_text)
        for event, elem in parser.read_events():
            if elem and elem.tag.endswith('title-info'):
                root = elem
            elif elem and elem.tag.endswith('publish-info'):
                root_second = elem
                break

    authors = list()
    for child in root:

        if child.tag.endswith('book-title'):
            title = child.text

        if child.tag.endswith('author'):
            author = str()
            for names in child:
                if names.tag.endswith('first-name') \
                        or names.tag.endswith('middle-name'):
                    if names.text is not None:
                        author = author + names.text + ' '
                elif names.tag.endswith('last-name'):
                    if names.text is not None:
                        author = author + names.text
            if author != '':
                authors.append(author)
    if bool(authors) is False:
        authors = 'NULL'
    else:
        authors = ','.join(authors)

    for child in root_second:
        if child.tag.endswith('year'):
            if child.text is not None:
                year = child.text
            else:
                year = 'NULL'

    return title, authors, year, book_path


def bookS_parser(book_paths):
    return [book_parser(path) for path in book_paths]


if __name__ == '__main__':
    args = parser.parse_args()
    book_paths = list()
    if args.s:
        if os.path.isdir(args.s):
            for dirname, subdirs, files in os.walk(args.s):
                if not dirname.endswith('/'):
                    dirname += '/'
                for file in files:
                    if file.endswith('.fb2')\
                            or file.endswith('.fb2.zip')\
                            or file.endswith('.fb2.gz'):
                        book_paths.append(dirname + file)
        else:
            print(f'Directory "{args.s}" does not exist')
    if args.a:
        if os.path.isfile(args.a):
            if args.a.endswith('.fb2')\
                    or args.a.endswith('.fb2.zip')\
                    or args.a.endswith('.fb2.gz'):
                book_paths.append(args.a)
        else:
            print(f'File "{args.a}" does not exist')

    data = bookS_parser(book_paths)
    connection, cursor = db.connect_db()

    if args.u:
        db.fill_and_update_table(cursor, data)
    else:
        db.fill_table(cursor, data)

    db.close_connection(connection, cursor)
