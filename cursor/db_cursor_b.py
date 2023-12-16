import datetime

import sqlalchemy as sa
from fastapi import Depends
from pydantic import BaseModel, Field

from app.utils import fastapi as fastapi_utils
from app.utils.sqla import db_execute

router = fastapi_utils.CustomAPIRouter(prefix="/course", tags=["course"])


class GetRequest(BaseModel):
    cursor: str | None
    count: int = Field(ge=1, le=20)


class GetResponse(BaseModel):
    class Course(BaseModel):
        id: int
        title: str
        created_datetime: datetime.datetime

    data: list[Course]
    next_cursor: str | None


@router.api_wrapper(
    "GET",
    "",
)
async def _(
        q: GetRequest = Depends(),
) -> GetResponse:
    courses = (
        (
            await db_execute(
                '''
                SELECT id, title, created_datetime
                FROM course
                ORDER BY created_datetime ASC, id ASC
                LIMIT :count
                ''',
                {
                    "count": q.count,
                },
            )
        )
            .fetchall()
    )

    return GetResponse(
        data=[
            GetResponse.Course(
                id=course.id,
                title=course.title,
                created_datetime=course.created_datetime,
            )
            for course in courses
        ],
        next_cursor=None,
    )