"""Database operations kept separate from HTTP route handlers."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Task, TaskPriority, TaskStatus, User
from app.schemas import TaskCreate, TaskUpdate


class UserAlreadyExistsError(Exception):
    """Raised when a user email conflicts with an existing account."""


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.scalar(select(User).where(User.email == email))


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def create_user(session: Session, email: str, hashed_password: str) -> User:
    user = User(email=email, hashed_password=hashed_password)
    session.add(user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise UserAlreadyExistsError from exc
    session.refresh(user)
    return user


def list_tasks(
    session: Session,
    owner_id: int,
    *,
    status: TaskStatus | None,
    priority: TaskPriority | None,
    offset: int,
    limit: int,
) -> list[Task]:
    statement = select(Task).where(Task.owner_id == owner_id)
    if status is not None:
        statement = statement.where(Task.status == status)
    if priority is not None:
        statement = statement.where(Task.priority == priority)
    statement = statement.order_by(Task.id).offset(offset).limit(limit)
    return list(session.scalars(statement).all())


def get_task(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)


def create_task(session: Session, owner_id: int, payload: TaskCreate) -> Task:
    task = Task(owner_id=owner_id, **payload.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(session: Session, task: Task, payload: TaskUpdate) -> Task:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
    session.commit()
