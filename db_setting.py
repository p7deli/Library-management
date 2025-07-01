import mysql.connector as conn
import datetime


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
            actual_return_date DATE DEFAULT NULL,
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
            return False, 'عضوی با این مشخصات یافت نشد ...'
        
        cursor.execute('''
            SELECT * FROM books WHERE book_id=%s;
        ''', (book_id,))

        book = cursor.fetchone()
        if not book:
            return False, 'کتابی با این مشخصات یافت نشد'
        
        if not book[-1]:
            return False, 'کتاب در دسترس نیست'
        
        cursor.execute('''
                INSERT INTO borrowings (member_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s);
            ''', (member_id, book_id, borrow_date, return_date))
        
        cursor.execute('''
                UPDATE books SET available=FALSE WHERE book_id=%s;
            ''', (book_id,))
        
        cnn.commit()
        cnn.close()
        return True, 'امانت با موفقیت ثبت شد'

    except Exception as e:
        print(f'Error\n{e}')
        cnn.rollback()
    finally:
        cnn.close()

def show_borrow_for_table():
    cursor, cnn = connection()

    cursor.execute('''SELECT borrowing_id, m.name, b.title, borrow_date, return_date 
                    FROM borrowings 
                    JOIN members m ON m.member_id=borrowings.member_id
                    JOIN books b ON b.book_id=borrowings.book_id''')
    borrows = [borrow for borrow in cursor]
    cnn.close()
    return borrows

def show_borrow_for_table_back_book():
    cursor, cnn = connection()

    cursor.execute('''SELECT borrowing_id, m.name, b.title, borrow_date, return_date, actual_return_date 
                    FROM borrowings 
                    JOIN members m ON m.member_id=borrowings.member_id
                    JOIN books b ON b.book_id=borrowings.book_id''')
    borrows = [borrow for borrow in cursor]
    cnn.close()
    return borrows

def show_member_nam_book_name():
    cursor, cnn = connection()

    cursor.execute('''SELECT member_id, name FROM members''')
    members = [str(name[0])+'.'+name[1] for name in cursor]

    cursor.execute('''SELECT book_id, title FROM books''')
    books = [str(name[0])+'.'+name[1] for name in cursor]

    cnn.close()
    return members, books

def delete_borrow_(borrow_id):
    cursor, cnn = connection()
    cursor.execute('''SELECT book_id FROM borrowings WHERE borrowing_id=%s;''', (borrow_id,))
    book_id = cursor.fetchone()[0]

    cursor.execute('''
                UPDATE books SET available=TRUE WHERE book_id=%s;
            ''', (book_id,))
    cnn.commit()

    cursor.execute('''DELETE FROM borrowings WHERE borrowing_id=%s;''', (borrow_id,))
    cnn.commit()

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
        cnn.close()
        return False, 'این کتاب در حال حاظر امانت داده شده'
    
    else:
        cursor.execute('''DELETE FROM books WHERE book_id=%s;''', (book_id,))
        cnn.commit()
        cnn.close()
        return True, 'کتاب با موفقیت حذف شد'


def back_book(borrowing_id):
    cursor, cnn = connection()
    cursor.execute('''SELECT book_id FROM borrowings WHERE borrowing_id=%s;''', (borrowing_id,))
    book_id = cursor.fetchone()[0]

    cursor.execute('''
                UPDATE books SET available=TRUE WHERE book_id=%s;
            ''', (book_id,))
    cnn.commit()

    today = datetime.datetime.today()
    cursor.execute('''
                UPDATE borrowings SET actual_return_date=%s WHERE borrowing_id=%s;
            ''', (today, borrowing_id))
    cnn.commit()
    cnn.close()


if __name__ == '__main__':
    print(show_borrow_for_table())