import psycopg2
from psycopg2 import Error
from config_read import user_db, password_db


def connect_db():

    try:
        con = psycopg2.connect(
            database='VKinder',
            user=user_db,
            password=password_db,
            host="127.0.0.1",
            port="5432"
        )

        with con.cursor() as cursor:
            cursor.execute("""SELECT table_name FROM information_schema.tables
                    WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
                    AND table_schema IN('public', 'myschema');
                    """)
            if not cursor.fetchall():
                cursor.execute('''create table IF NOT exists Users(
                                    id_user_VK INTEGER primary key,
                                    nikname VARCHAR(50),
                                    birthday VARCHAR(10),
                                    gender VARCHAR(7),
                                    city_id INTEGER,
                                    city_title VARCHAR(30)	
                                    );
                                    ''')

                cursor.execute('''create table IF NOT exists Find_Users(
                                    id_find SERIAL primary key,
                                    id_vk INTEGER unique,
                                    nikname VARCHAR(50),
                                    link_profile VARCHAR(256),
                                    link_photo1 VARCHAR(256),
                                    link_photo2 VARCHAR(256),
                                    link_photo3 VARCHAR(256)
                                    );
                                    ''')
                cursor.execute('''create table if not exists Links(
                                    id SERIAL primary key,
                                    id_user INTEGER REFERENCES Users(id_user_VK),
                                    id_find INTEGER REFERENCES Find_users(id_find),
                                    chosen BOOLEAN DEFAULT FALSE,
                                    blacklist BOOLEAN DEFAULT FALSE
                                    );
                                    ''')
                con.commit()
                print("Таблицы успешно созданы в PostgreSQL")
            else:
                print('Подключение к базе данных прошло успешно')
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    return con

def insert_user(user_list):
    con = connect_db()
    with con.cursor() as cursor:
        cursor.execute("""select * from users where id_user_VK=%s;""",(user_list[4],))
        if not cursor.fetchall():
            cursor.execute("""
                    INSERT INTO users(id_user_Vk,nikname, birthday,gender,city_id, city_title)
                    VALUES(%s, %s, %s, %s,%s, %s);
                    """, (user_list[4],user_list[2],user_list[3],user_list[1],user_list[0]['id'],user_list[0]['title']))
        con.commit()
