from sqlalchemy import select

from app.database import create_database
from app.models import Base, Task, User


def test_sqlite_database_enforces_foreign_keys_and_cascades_user_deletion(tmp_path):
    database_url = f"sqlite:///{(tmp_path / 'cascade.db').as_posix()}"
    engine, session_factory = create_database(database_url)
    Base.metadata.create_all(bind=engine)

    session = session_factory()
    try:
        user = User(email="cascade@example.com", hashed_password="test-hash")
        session.add(user)
        session.flush()
        task = Task(owner_id=user.id, title="Owned task")
        session.add(task)
        session.commit()

        session.delete(user)
        session.commit()

        assert session.scalar(select(Task)) is None
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_sqlite_foreign_key_pragma_is_enabled(tmp_path):
    database_url = f"sqlite:///{(tmp_path / 'pragma.db').as_posix()}"
    engine, _ = create_database(database_url)
    try:
        with engine.connect() as connection:
            assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
    finally:
        engine.dispose()
