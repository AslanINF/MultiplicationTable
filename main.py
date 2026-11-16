import sqlite3

# 1. Свързване с базата данни
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# 2. Създаване на таблиците
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year_published INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    grade TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Borrowings (
    borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    book_id INTEGER,
    borrow_date TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
)
''')

# 3. Вмъкване на данни
cursor.executemany('''INSERT INTO Books (title, author, year_published) VALUES (?, ?, ?)''', [
    ('Под игото', 'Иван Вазов', 1894),
    ('Малкият принц', 'Антоан дьо Сент-Екзюпери', 1943),
    ('Хари Потър и Философският камък', 'Дж. К. Роулинг', 1997)
])

cursor.executemany('''INSERT INTO Students (first_name, last_name, grade) VALUES (?, ?, ?)''', [
    ('Иван', 'Петров', '10А'),
    ('Мария', 'Иванова', '10А'),
    ('Георги', 'Тодоров', '11Б')
])

cursor.executemany('''INSERT INTO Borrowings (student_id, book_id, borrow_date) VALUES (?, ?, ?)''', [
    (1, 2, '2026-10-15'), # Иван взима Малкият принц
    (2, 1, '2026-10-20')  # Мария взима Под игото
])

conn.commit()

# 4. Примерна заявка (JOIN)
print("--- Справка за заети книги ---")
cursor.execute('''
SELECT Students.first_name, Students.last_name, Books.title 
FROM Borrowings
JOIN Students ON Borrowings.student_id = Students.student_id
JOIN Books ON Borrowings.book_id = Books.book_id
''')

for row in cursor.fetchall():
    print(f"{row[0]} {row[1]} зае книгата '{row[2]}'")

conn.close()
