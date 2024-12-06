import psycopg2
from psycopg2 import sql, DatabaseError, OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from decouple import config
import logging

# تنظیمات لاگر
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_user(connection, db_user, db_password):
    """
    ایجاد یوزر در صورت عدم وجود
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT 1 FROM pg_roles WHERE rolname = %s;"),
                [db_user]
            )
            if not cursor.fetchone():
                cursor.execute(
                    sql.SQL("CREATE USER {} WITH PASSWORD %s;").format(
                        sql.Identifier(db_user)
                    ),
                    [db_password]
                )
                logger.info(f"User '{db_user}' created successfully.")
            else:
                logger.info(f"User '{db_user}' already exists.")
    except DatabaseError as e:
        logger.error(f"Error while creating user '{db_user}': {e}")
        raise

def create_database(db_name, db_user, postgres_password, db_host, db_port):
    """
    ایجاد دیتابیس در صورت عدم وجود
    """
    connection = None
    try:
        # اتصال به دیتابیس PostgreSQL پیش‌فرض
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=postgres_password,
            host=db_host,
            port=db_port,
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"),
                [db_name]
            )
            if not cursor.fetchone():
                # اجرای دستور CREATE DATABASE
                cursor.execute(
                    sql.SQL("CREATE DATABASE {} OWNER {};").format(
                        sql.Identifier(db_name),
                        sql.Identifier(db_user)
                    )
                )
                logger.info(f"Database '{db_name}' created successfully.")
            else:
                logger.info(f"Database '{db_name}' already exists.")
    except DatabaseError as e:
        logger.error(f"Error while creating database '{db_name}': {e}")
        raise
    finally:
        if connection:
            connection.close()

def setup_database():
    """
    تنظیم دیتابیس و یوزر با مدیریت کامل خطاها
    """
    db_name = config('DATABASE_NAME', default='crm_db')
    db_user = config('DATABASE_USER', default='crm_user')
    db_password = config('DATABASE_PASSWORD', default='crm_password')
    db_host = config('DATABASE_HOST', default='localhost')
    db_port = config('DATABASE_PORT', default='5432')
    postgres_password = config('POSTGRES_PASSWORD', default='postgres_password')

    try:
        # اتصال به دیتابیس PostgreSQL پیش‌فرض برای ایجاد یوزر
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=postgres_password,
            host=db_host,
            port=db_port,
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # ایجاد یوزر
        create_user(connection, db_user, db_password)

        # ایجاد دیتابیس
        create_database(db_name, db_user, postgres_password, db_host, db_port)

    except OperationalError as e:
        logger.error(f"Operational error during database setup: {e}")
        raise
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    try:
        setup_database()
    except Exception as e:
        logger.critical(f"Setup failed: {e}")
