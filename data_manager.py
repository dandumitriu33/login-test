import database_common
import psycopg2
import bcrypt


@database_common.connection_handler
def get_cars(cursor):
    cursor.execute(f"""
                        SELECT name, cars FROM users
                        ORDER BY name ASC; 
        """)
    cars = cursor.fetchall()
    return cars


@database_common.connection_handler
def register_user(cursor, name, username, email, cars, password):
    cursor.execute(f"""
                        INSERT INTO users (name, username, email, cars, password)
                        VALUES ('{name}', '{username}', '{email}', '{cars}', '{password}');
""")


def get_salt():
    return bcrypt.gensalt()


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')
