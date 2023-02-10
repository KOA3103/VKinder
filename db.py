import psycopg2 as pg
from config import host, user, password, db_name


with pg.connect(
    host=host,  # 127.0.0.1
    user=user,  # postgres
    password=password,  # postgres
    database=db_name  # postgres
) as conn:
    conn.autocommit = True


def create_table_found_person():
    """create table found_person"""
    with conn.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS found_person(
                id serial,
                first_name varchar(50) NOT NULL,
                last_name varchar(25) NOT NULL,
                id_vk varchar(20) NOT NULL PRIMARY KEY,
                vk_link varchar(50),
                request_from varchar(20) NOT NULL);"""

        )


def create_table_seen_person():  # references users(id_vk)
    """create table seen_person"""
    with conn.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS seen_person(
            id serial,
            id_vk varchar(50) PRIMARY KEY);"""
        )


def insert_found_person(first_name, last_name, id_vk, vk_link, request_from):
    """insert info from looking_for_persons into table found_person"""
    with conn.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO found_person (first_name, last_name, id_vk, vk_link, request_from) 
            VALUES (%s, %s, %s, %s, %s)""",
            (first_name, last_name, id_vk, vk_link, request_from)
        )


def insert_data_seen_person(id_vk, offset):
    """inserting data into the seen_users table"""
    with conn.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO seen_person (id_vk) 
            VALUES ('{id_vk}')
            OFFSET '{offset}';"""
        )

def check():
    with conn.cursor() as cursor:
        cursor.execute(
            f"""SELECT fp.id_vk 
            FROM found_person AS fp;"""
        )
        return cursor.fetchall()



def select(offset):
    """select of unreviewed people"""
    with conn.cursor() as cursor:
        cursor.execute(
            f"""SELECT 
            fp.first_name,
            fp.last_name,
            fp.id_vk,  
            fp.vk_link,
            sp.id_vk
            FROM found_person AS fp
            LEFT JOIN seen_person AS sp 
            ON fp.id_vk = sp.id_vk
            WHERE sp.id_vk IS NULL
            OFFSET '{offset}';"""

        )
        return cursor.fetchone()


def delete_table_found_person():
    """delete table found_person by cascade"""
    with conn.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS found_person CASCADE;"""
        )


def delete_table_seen_person():
    """delete table seen_person by cascade"""
    with conn.cursor() as cursor:
        cursor.execute(
            """DROP TABLE  IF EXISTS seen_person CASCADE;"""
        )


def creating_database():
    delete_table_found_person()
    delete_table_seen_person()
    create_table_found_person()
    create_table_seen_person()
    print("Database was created!")

# db = creating_database()
# delete_table_found_person()
# delete_table_seen_person()
# create_table_found_person()
# create_table_seen_person()
# creating_database()