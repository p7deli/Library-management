import mysql.connector as conn


def connection():
    con = conn.connect(
    host='localhost',
    user='admin',
    password='1234',
    database='library_db'
    )

    cursor = con.cursor()
    return cursor, con


def create_tables():
    cursor, conn = connection()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members(
            member_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20)
            )
    ''')

    conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books(
            book_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200),
            author VARCHAR(100),
            isbn VARCHAR(20),
            available BOOLEAN DEFAULT TRUE)    
    ''')

    conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrowings (
            borrowing_id INT AUTO_INCREMENT PRIMARY KEY,
            member_id INT,
            book_id INT,
            borrow_date DATE,
            return_date DATE,
            FOREIGN KEY (member_id) REFERENCES members(member_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id))
    ''')

    conn.commit()
    conn.close()


def add_members(name, email, phone):
    cursor, cnn = connection()

    cursor.execute('''
        INSERT INTO members (name, email, phone) VALUES(%s, %s, %s);
    ''', (name, email, phone))

    cnn.commit()
    cnn.close()

def show_members_for_table():
    cursor, cnn = connection()

    cursor.execute('''
        SELECT * FROM members;
    ''')

    result = [item for item in cursor]
    cnn.close()
    return result


def add_books(title, author, isbn):
    cursor, cnn = connection()

    cursor.execute('''
        INSERT INTO books (title, author, isbn) VALUES(%s, %s, %s);
    ''', (title, author, isbn))

    cnn.commit()
    cnn.close()

def show_books_for_table():
    cursor, cnn = connection()

    cursor.execute('''
        SELECT * FROM books;
    ''')

    result = [item for item in cursor]
    cnn.close()
    return result

def add_borrow(member_id, book_id, borrow_date, return_date):
    cursor, cnn = connection()

    try:
        cursor.execute('''
            SELECT * FROM members WHERE member_id=%s;
        ''', (member_id,))
        
        member = cursor.fetchone()
        if not member:
            print('Error, member not found ...')
            return
        
        cursor.execute('''
            SELECT * FROM books WHERE book_id=%s;
        ''', (book_id,))

        book = cursor.fetchone()
        if not book:
            print('Error, book not found ...')
            return
        
        if not book[-1]:
            print('Error, book not available ...')
            return
        
        cursor.execute('''
                INSERT INTO borrowings (member_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s);
            ''', (member_id, book_id, borrow_date, return_date))
        
        cursor.execute('''
                UPDATE books SET available=FALSE WHERE book_id=%s;
            ''', (book_id,))
        
        cnn.commit()
        cnn.close()
        print('add borrow successfully.')

    except Exception as e:
        print(f'Error\n{e}')
        cnn.rollback()
    finally:
        cnn.close()


def delete_members(member_id):
    cursor, cnn = connection()

    cursor.execute('''SELECT * FROM borrowings WHERE member_id=%s;''', (member_id,))
    member = cursor.fetchone()

    if member:
        print('Error, member is in the existing borrowings table')
        return
    
    cursor.execute('''DELETE FROM members WHERE member_id=%s;''', (member_id,))
    cnn.commit()
    cnn.close()


def delete_books(book_id):
    cursor, cnn = connection()

    cursor.execute('''SELECT * FROM borrowings WHERE book_id=%s;''', (book_id,))
    book = cursor.fetchone()

    if book:
        print('Error, book is in the existing borrowings table')
        return
    
    cursor.execute('''DELETE FROM books WHERE book_id=%s;''', (book_id,))
    cnn.commit()
    cnn.close()


def back_book(book_id):
    cursor, cnn = connection()

    cursor.execute('''SELECT * FROM borrowings WHERE book_id=%s;''', (book_id,))
    borrow = cursor.fetchone()

    if borrow:
        cursor.execute('''DELETE FROM borrowings WHERE book_id=%s;''', (book_id,))
        cnn.commit()
        cursor.execute('''
                UPDATE books SET available=TRUE WHERE book_id=%s;
            ''', (book_id,))
        cnn.commit()

        cnn.close()

        print('book back successfully')
    else:
        print('Error, book not found')


if __name__ == '__main__':
    print(show_books_for_table())