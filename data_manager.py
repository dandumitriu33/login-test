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


@database_common.connection_handler
def get_db_password_for_user(cursor, username):
    cursor.execute(f"""
                       SELECT password FROM users
                       WHERE username='{username}';
    """)
    result = cursor.fetchone()
    hashed_password = result['password']
    return hashed_password


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def get_user_id_by_username(cursor, username):
    cursor.execute(f"""
                        SELECT id FROM users
                        WHERE username='{username}';
""")
    result = cursor.fetchone()
    user_id = result['id']
    return user_id


@database_common.connection_handler
def add_message(cursor, message, user_id):
    cursor.execute(f"""
                        INSERT INTO messages (message, user_id)
                        VALUES ('{message}', {user_id});
    """)


@database_common.connection_handler
def get_all_messages(cursor):
    cursor.execute(f"""
                            SELECT * FROM messages
                            ORDER BY created DESC; 
            """)
    messages = cursor.fetchall()
    return messages
