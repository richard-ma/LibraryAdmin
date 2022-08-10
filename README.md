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
  * bo_id [foreign key -> book:id]
  * status
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
* \>\> .tables [display some talbe name like book, borrow, store]
* \>\> .quit