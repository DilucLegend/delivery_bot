import sqlite3

connection = sqlite3.connect('anime_list.db')

sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS anime_list(photo TEXT, anime_name TEXT, genres TEXT, anime_description TEXT, url TEXT);')

sql.execute('CREATE TABLE IF NOT EXISTS user_genre_list(tg_id INTEGER, genres TEXT);')

def adding_anime_to_database(photo, anime_name, genres, anime_description, url):

    connection = sqlite3.connect('anime_list.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO anime_list (photo, anime_name, genres, anime_description, url) VALUES (?,?,?,?,?);',(photo, anime_name, genres, anime_description, url))

    connection.commit()

def adding_genre_to_user_genre_list(genres, tg_id):
    connection = sqlite3.connect('anime_list.db')
    sql = connection.cursor()

    a = sql.execute('SELECT genres FROM user_genre_list WHERE genres IS NOT NULL AND tg_id=?;',(tg_id, ))
    for i in a:
        genres += i
    sql.execute('INSERT INTO user_genre_list (genres) VALUES (?) WHERE tg_id=?;', (genres, tg_id))

    connection.commit()

def clearing_user_genre_list(tg_id):

    connection = sqlite3.connect('anime_list.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM user_genre_list WHERE tg_id=?;', (tg_id, ))

    connection.commit()

def deleting_exact_anime_from_database(anime_name):

    connection = sqlite3.connect('anime_list.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM anime_list * WHERE anime_name=?;', (anime_name))

    connection.commit()

def get_user_genre_list(tg_id):

    connection = sqlite3.connect('anime_list.db')
    sql = connection.cursor()

    a = sql.execute('SELECT genres FROM user_genre_list WHERE tg_id=?;', (tg_id, ))

    return a

def abc():
    connection = sqlite3.connect('anime_list.db')
    sql = connection.cursor()
    # sql.execute('TRUNCATE TABLE user_genre_list;')
    sql.execute('TRUNCATE TABLE anime_list;')

abc()