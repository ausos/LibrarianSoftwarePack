DROP TABLE IF EXISTS books;

CREATE TABLE books(
    number SERIAL PRIMARY KEY,
    author VARCHAR,
    book_name VARCHAR,
    year VARCHAR,
    book_path VARCHAR UNIQUE
);