import argparse
import data_base as db

parser = argparse.ArgumentParser(description='Delete book or clear whole library')
parser.add_argument('-n', help='Book number')
parser.add_argument('-a', default=False, action='store_true',
                    help='Delete all')

if __name__ == '__main__':
    args = parser.parse_args()
    connection, cursor = db.connect_db()
    if args.n:
        db.delete_by_number(cursor,connection, args.n)
    else:
        print('Add the book number to delete in argument "-n"')
    if args.a:
        db.delete_all(cursor, connection)

    db.close_connection(connection, cursor)
