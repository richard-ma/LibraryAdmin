DROP TABLE IF EXISTS book;
CREATE TABLE book (
    id TEXT PRIMARY KEY,
    name TEXT,
    author TEXT,
    publisher  TEXT,
    isbn TEXT,
    image TEXT,
    flag TEXT
);

DROP TABLE IF EXISTS audience;
CREATE TABLE audience(
    id TEXT PRIMARY KEY,
    password TEXT
);

DROP TABLE IF EXISTS admin;
CREATE TABLE admin(
    id TEXT PRIMARY KEY,
    password TEXT
);

DROP TABLE IF EXISTS store;
CREATE TABLE store (
    id TEXT PRIMARY KEY,
    book_id TEXT REFERENCES book(id) ON DELETE CASCADE ON UPDATE CASCADE,
    status TEXT,
    flag TEXT
);

DROP TABLE IF EXISTS borrow;
CREATE TABLE borrow (
    id TEXT PRIMARY KEY,
    store_id TEXT REFERENCES store(id) ON DELETE CASCADE ON UPDATE CASCADE,
    audience_id TEXT REFERENCES audience(id) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO admin VALUES('admin', 'admin');