import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from decouple import config

def setup_database():
    db_name = config('DATABASE_NAME', default='crm_db')
    db_user = config('DATABASE_USER', default='crm_user')
    db_password = config('DATABASE_PASSWORD', default='crm_password')
    db_host = config('DATABASE_HOST', default='localhost')
    db_port = config('DATABASE_PORT', default='5432')
    connection = None

    try:
        # اتصال به PostgreSQL
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=config('POSTGRES_PASSWORD', default='postgres_password'),
            host=db_host,
            port=db_port,
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        # بررسی اینکه آیا دیتابیس وجود دارد یا نه
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
        exists = cursor.fetchone()

        if not exists:
            # ایجاد یوزر و دیتابیس در صورت عدم وجود
            cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}';")
            cursor.execute(f"CREATE DATABASE {db_name} OWNER {db_user};")
            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};")
            print(f"Database '{db_name}' and user '{db_user}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")

    except Exception as e:
        print(f"Error during database setup: {e}")

    finally:
        if connection:
            connection.close()

# اجرای تابع
setup_database()
