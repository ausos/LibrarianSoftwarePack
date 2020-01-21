import argparse
import data_base as db

parser = argparse.ArgumentParser(description='Search book by author, title, year')
parser.add_argument('-a', help='Author name')
parser.add_argument('-n', help='Book name')
parser.add_argument('-y', help='Year')
parser.add_argument('-s', default=False, action='store_true',
                    help='Output only unique identifier of the book')

if __name__ == '__main__':
    args = parser.parse_args()

    conditions = dict()
    if args.a:
        conditions['author'] = args.a
    else:
        conditions['author'] = ''
    if args.n:
        conditions['book_name'] = args.n
    else:
        conditions['book_name'] = ''
    if args.y:
        conditions['year'] = args.y
    else:
        conditions['year'] = ''

    if args.a or args.n or args.y:
        connection, cursor = db.connect_db()
        if args.s:
            db.search_book_number(cursor, conditions)
            print(cursor.fetchall())
        else:
            db.search_book(cursor, conditions)
            print(cursor.fetchall())
        db.close_connection(connection, cursor)
    else:
        print('Add book search criteria')
