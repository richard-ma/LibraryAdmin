# LibraryAdmin

## database
* book
  * id
  * name
  * author
  * publisher
  * isbn
  * image
  * flag
* audience
  * id
  * password
* store
  * id
  * book_id [foreign key -> book:id]
  * status [0: on shelf; 1: be borrowed]
  * flag
* borrow
  * id
  * store_id [foreign key -> store:id]
  * audience_id [foreign key -> audience:id]

## Route
* /
* /book
  * /new
  * /update
    * id
  * /delete
    * id
  * /search
    * name
    * author
    * publisher
* /audience
  * /register
  * /login
    * id
    * password
  * /logout
    * id
* /store
  * /new
    * book_id
  * /update
    * id
  * /delete
    * id
  * /search
    * id

## Install
* sqlite3 ./data/libraryadmin.db ".read /path/to/LibraryAdmin/data/init_db.sql"
* sqlite3 ./data/libraryadmin.db
* \>\> .tables `display some talbe name like book, borrow, store, etc. check tables`
* \>\> .mode csv `import dev data to database`
* \>\> .import absolut/path/to/LibraryAdmin/data/dev_data/books.csv book `import some book data`
* \>\> .import absolut/path/to/LibraryAdmin/data/dev_data/audiences.csv andience`import admin id and password`
* \>\> .quit