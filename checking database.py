import sqlite3 as sq

with sq.connect('expense_database.db') as con:
    cur = con.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    print('users table')
    for user in users:
        print(*user)
    print()
    cur.execute('SELECT * FROM categories')
    categories = cur.fetchall()
    print('categories table')
    for cat in categories:
        print(*cat)
    print()
    cur.execute('SELECT * FROM expenses')
    expenses = cur.fetchall()
    print('expenses table')
    for exp in expenses:
        print(*exp)
    print()
    cur.close()