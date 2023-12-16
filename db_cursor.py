import datetime

import sqlalchemy as sa
from fastapi import Depends
from pydantic import BaseModel, Field

from app.utils import fastapi as fastapi_utils
from app.utils.sqla import db_execute
from typing import Optional, Tuple

router = fastapi_utils.CustomAPIRouter(prefix="/course", tags=["course"])


class GetRequest(BaseModel):
    cursor: Optional[str] = None
    count: int = Field(ge=1, le=20)


class GetResponse(BaseModel):
    class Course(BaseModel):
        id: int
        title: str
        created_datetime: datetime.datetime

    data: list[Course]
    next_cursor: Optional[str]


@router.api_wrapper(
    "GET",
    "",
)
async def _(
        q: GetRequest = Depends(),
) -> GetResponse:
    cursor_datetime, cursor_id = datetime.datetime.min, 0
    if q.cursor:
        cursor_datetime_str, cursor_id_str = q.cursor.split(',')
        cursor_datetime = datetime.datetime.fromisoformat(cursor_datetime_str)
        cursor_id = int(cursor_id_str)
    courses = (
        (
            await db_execute(
                '''
                SELECT id, title, created_datetime
                FROM course
                WHERE (created_datetime, id) > (:cursor_datetime, :cursor_id)
                ORDER BY created_datetime ASC, id ASC
                LIMIT :count
                ''',
                {
                    "cursor_datetime": cursor_datetime,
                    "cursor_id": cursor_id,
                    "count": q.count,
                },
            )
        )
            .fetchall()
    )
    next_cursor = None
    if courses:
        next_cursor = f"{courses[-1].created_datetime.isoformat()},{courses[-1].id}"

    return GetResponse(
        data=[
            GetResponse.Course(
                id=course.id,
                title=course.title,
                created_datetime=course.created_datetime,
            )
            for course in courses
        ],
        next_cursor=next_cursor,
    )