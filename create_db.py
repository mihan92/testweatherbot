# pip istall sqlite3
import sqlite3
import telebot

connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()

def create_db():
    cursor.execute('''create table if not exists users(
        user_id integer,
        username text,
        firstname text,
        city text
    )
    ''')
    connect.commit()

def user_add(user_id: int, username: str, firstname: str, city: str):
    cursor.execute('INSERT INTO users VALUES(?,?,?,?)', (user_id, username, firstname, city))
    connect.commit()



def city_edit(user_id: int, city: str):
    user_id = user_id
    city = city
    edit = f"UPDATE users SET user_id = '{user_id}' WHERE user_id = {user_id}"
    cursor.execute(edit)
    connect.commit()

