import uuid
import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    db_host = os.environ["INSTANCE_HOST"]
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_port = os.environ["DB_PORT"]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
    )
    return pool

def add_user_upload_record(data) -> None:
    engine = connect_tcp_socket()

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        insert_query = text("""
            INSERT INTO user_upload (id, email, image, transcript, text_path)
            VALUES (:id, :email, :image, :transcript, :text_path)
        """)

        session.execute(insert_query, {
            'id': str(uuid.uuid4()),
            'email': data['email'],
            'image': data['image_path'],
            'transcript': data['transcript'],
            'text_path': data['text_path']
        })

        session.commit()

    except Exception as e:
        session.rollback()
        print(f"An error occurred while adding record: {e}")

    finally:
        session.close()

def fetch_user_uploads_by_email(email: str):
    engine = connect_tcp_socket()

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        select_query = text("""
            SELECT id, email, image, transcript, text_path
            FROM user_upload
            WHERE email = :email
        """)

        results = session.execute(select_query, {'email': email}).fetchall()

        if results:
            return [
                {
                    'id': result[0],
                    'email': result[1],
                    'image': result[2],
                    'transcript': result[3],
                    'text_path': result[4]
                }
                for result in results
            ]
        else:
            return []

    except Exception as e:
        print(f"An error occurred while fetching records: {e}")
        return []

    finally:
        session.close()
