"""Authenticated task-management endpoints."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import crud
from app.dependencies import CurrentUser, DatabaseSession
from app.models import Task, TaskPriority, TaskStatus
from app.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    responses={401: {"description": "Missing or invalid bearer token."}},
)
def create_task(
    payload: TaskCreate,
    current_user: CurrentUser,
    session: DatabaseSession,
) -> TaskRead:
    task = crud.create_task(session, current_user.id, payload)
    return TaskRead.model_validate(task)


@router.get(
    "",
    response_model=list[TaskRead],
    summary="List the current user's tasks",
    description="Filter by status or priority and paginate with offset and limit.",
    responses={401: {"description": "Missing or invalid bearer token."}},
)
def read_tasks(
    current_user: CurrentUser,
    session: DatabaseSession,
    task_status: Annotated[TaskStatus | None, Query(alias="status")] = None,
    priority: TaskPriority | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[TaskRead]:
    task_records = crud.list_tasks(
        session, current_user.id, status=task_status, priority=priority,
        offset=offset, limit=limit
    )
    return [TaskRead.model_validate(task) for task in task_records]


@router.get(
    "/{task_id}",
    response_model=TaskRead,
    summary="Get one task",
    description="An existing task owned by another account returns 403 Forbidden.",
    responses={
        401: {"description": "Missing or invalid bearer token."},
        403: {"description": "The task belongs to another user."},
        404: {"description": "No task exists with this ID."},
    },
)
def read_task(
    task_id: int,
    current_user: CurrentUser,
    session: DatabaseSession,
) -> TaskRead:
    task = get_owned_task(session, task_id, current_user.id)
    return TaskRead.model_validate(task)


@router.patch(
    "/{task_id}",
    response_model=TaskRead,
    summary="Update a task",
    description="Update one or more task fields, including status to mark it pending or completed.",
    responses={
        401: {"description": "Missing or invalid bearer token."},
        403: {"description": "The task belongs to another user."},
        404: {"description": "No task exists with this ID."},
    },
)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    current_user: CurrentUser,
    session: DatabaseSession,
) -> TaskRead:
    task = get_owned_task(session, task_id, current_user.id)
    updated_task = crud.update_task(session, task, payload)
    return TaskRead.model_validate(updated_task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    responses={
        401: {"description": "Missing or invalid bearer token."},
        403: {"description": "The task belongs to another user."},
        404: {"description": "No task exists with this ID."},
    },
)
def delete_task(
    task_id: int,
    current_user: CurrentUser,
    session: DatabaseSession,
) -> Response:
    task = get_owned_task(session, task_id, current_user.id)
    crud.delete_task(session, task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_owned_task(session: Session, task_id: int, owner_id: int) -> Task:
    task = crud.get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    if task.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this task.",
        )
    return task
