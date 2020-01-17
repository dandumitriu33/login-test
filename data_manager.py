import database_common
import psycopg2


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
