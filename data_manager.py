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
