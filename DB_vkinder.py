import psycopg2
from psycopg2 import Error
from config_read import user_db, password_db


def connect_db():
    #подключение к БД
    try:
        con = psycopg2.connect(
            database='VKinder',
            user=user_db,
            password=password_db,
            host="127.0.0.1",
            port="5432"
        )
        with con.cursor() as cursor:
            # проверка на наличе таблиц в БД
            cursor.execute("""SELECT table_name FROM information_schema.tables
                    WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
                    AND table_schema IN('public', 'myschema');
                    """)
            if not cursor.fetchall(): #если в БД нет таблиц, то они создаются
                create_tables(cursor, con)
            else:
                print('Подключение к базе данных прошло успешно')
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    return con


def insert_user(user_list):
    # добавлет пользователя, который начал общение с ботом
    con = connect_db()
    with con.cursor() as cursor:
        cursor.execute("""select * from users where id_user_VK=%s;""",(user_list[4],))
        if not cursor.fetchall():
            cursor.execute("""
                    INSERT INTO users(id_user_Vk,nikname, birthday,gender,city_id, city_title)
                    VALUES(%s, %s, %s, %s,%s, %s);
                    """, (user_list[4],user_list[2],user_list[3],user_list[1],user_list[0]['id'],user_list[0]['title']))
        con.commit()
    con.close()


def insert_find(profile_list):
    # добавление предложенного профеля
    con = connect_db()
    with con.cursor() as cursor:
        cursor.execute("""
                        INSERT INTO find_users(id_vk,nikname,link_profile,attachment)
                        VALUES(%s, %s, %s, %s);
                        """, (
                        profile_list[0]['id'],profile_list[0]['name'],
                        profile_list[0]['link_id'],profile_list[0]['attachment']))
        con.commit()
        cursor.execute("Select max(id_find) from find_users;")
        idf = cursor.fetchone()[0]
        cursor.execute("select * from links where id_user=%s and id_find=%s;", (profile_list[0]['user_id'],idf))
        if not cursor.fetchall():
            cursor.execute("""
                        INSERT INTO links(id_user,id_find)
                        VALUES(%s, %s);
                        """, (
                        profile_list[0]['user_id'], idf))
        con.commit()
    con.close()


def add_elect(profile_list):
    # добавление пометки избранный
    con = connect_db()
    with con.cursor() as cursor:
        cursor.execute("Select max(id_find) from find_users;")
        idf = cursor.fetchone()[0]
        cursor.execute("UPDATE links SET chosen=%s WHERE id_user=%s and id_find=%s;",
                       (True, profile_list[0]['user_id'], idf))
        con.commit()
    con.close()


def select_elect(user):
    # выбор всех избранных для текущего пользователя
    con = connect_db()
    with con.cursor() as cursor:
        cursor.execute('''select
                        fu.id_vk, fu.nikname, fu.link_profile, fu.attachment, l.id_user
                        from links l, find_users fu
                        where l.id_user = %s and l.chosen = 'T' and l.id_find = fu.id_find''', (user,))
        persons = []
        for row in cursor.fetchall():
            dict_person = {'id': row[0], 'name': row[1], 'link_id': row[2], 'attachment': None, 'user_id': row[4]}
            persons.append(dict_person)
        return persons


def create_tables(cur,con):
    # создание таблиц в БД
    cur.execute('''create table IF NOT exists Users(
                                        id_user_VK INTEGER primary key,
                                        nikname VARCHAR(50) not null,
                                        birthday VARCHAR(10) not null,
                                        gender VARCHAR(7) not null,
                                        city_id INTEGER not null,
                                        city_title VARCHAR(30) not null
                                        );
                                        ''')

    cur.execute('''create table IF NOT exists Find_Users(
                                        id_find SERIAL primary key,
                                        id_vk INTEGER not null,
                                        nikname VARCHAR(50) not null,
                                        link_profile VARCHAR(256) not null,
                                        attachment VARCHAR(256) not null
                                        );
                                        ''')
    cur.execute('''create table if not exists Links(
                                        id SERIAL primary key,
                                        id_user INTEGER REFERENCES Users(id_user_VK),
                                        id_find INTEGER REFERENCES Find_users(id_find),
                                        chosen BOOLEAN DEFAULT FALSE,
                                        blacklist BOOLEAN DEFAULT FALSE
                                        );
                                        ''')
    con.commit()
    print("Таблицы успешно созданы в PostgreSQL")