import configparser
import psycopg2
import psycopg2.extras


def connect_db():
    user = 'myuser'
    password = 'mypasswd'
    host = 'localhost'
    port = '5432'

    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'pgsql' in config:
        if 'user' in config['pgsql']:
            user = config['pgsql']['user']
        if 'password' in config['pgsql']:
            password = config['pgsql']['password']
        if 'host' in config['pgsql']:
            host = config['pgsql']['host']
        if 'port' in config['pgsql']:
            port = config['pgsql']['port']

    try:
        conn = psycopg2.connect(
               user=user,
               password=password,
               host=host,
               port=port)
        print("Database opened successfully")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        raise
    return conn, conn.cursor()


def close_connection(conn, cur):
    if conn:
        conn.commit()
        cur.close()
        conn.close()


def fill_table(cur,book):
    psycopg2.extras.execute_values(cur, '''
    INSERT INTO books(
    book_name,
    author,
    year,
    book_path)
    VALUES %s
    ON CONFLICT (book_path) DO NOTHING
    ''', book, page_size=1000)
    print(cur.statusmessage)


def fill_and_update_table(cur,book):
    psycopg2.extras.execute_values(cur, '''
    INSERT INTO books(
    book_name,
    author,
    year,
    book_path)
    VALUES %s
    ON CONFLICT (book_path) DO UPDATE 
    SET book_name = excluded.book_name,
        author = excluded.author,
        year = excluded.year,
        book_path = excluded.book_path
    ''', book, page_size=1000)
    print(cur.statusmessage)


def delete_all(cur,conn):
    cur.execute("DELETE FROM Books")
    conn.commit()
    print(cur.statusmessage)


def delete_by_number(cur,conn, number):
    cur.execute(f"DELETE FROM Books WHERE number = {number}")
    conn.commit()
    print(cur.statusmessage)


def search_book(cur, condition):
    cur.execute(f'''
    SELECT * FROM books
    WHERE author LIKE '%{condition['author']}%' 
    AND book_name LIKE '%{condition['book_name']}%' 
    AND year LIKE '%{condition['year']}%'
    ''')
    print(cur.statusmessage)

def search_book_number(cur, condition):
    cur.execute(f'''
    SELECT number FROM books
    WHERE author LIKE '%{condition['author']}%' 
    AND book_name LIKE '%{condition['book_name']}%' 
    AND year LIKE '%{condition['year']}%'
    ''')
    print(cur.statusmessage)


