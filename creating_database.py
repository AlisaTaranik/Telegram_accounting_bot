import sqlite3 as sq

with sq.connect('expense_database.db') as con:
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY autoincrement, tg_user_id INT, user_language VARCHAR(2))')
    cur.execute('CREATE TABLE IF NOT EXISTS categories (category_id INTEGER PRIMARY KEY autoincrement, category_name VARCHAR(30), user_id INT, category_status INT)')
    cur.execute('CREATE TABLE IF NOT EXISTS expenses (expense_id INTEGER PRIMARY KEY autoincrement, expense DECIMAL(10, 2), expense_year INT, expense_month INT, expense_name_month VARCHAR(10), user_id INT, category_id INT)')
    con.commit()
    cur.close()

# It's code for creating a database named "Expenses" and having the same structure as in expenses_db_schema.png file