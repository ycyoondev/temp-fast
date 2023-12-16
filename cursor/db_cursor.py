# 필요한 라이브러리 및 모듈을 임포트합니다.
import datetime
import sqlalchemy as sa
from fastapi import Depends
from pydantic import BaseModel, Field
from app.utils import fastapi as fastapi_utils
from app.utils.sqla import db_execute
from typing import Optional, Tuple

# FastAPI의 라우터를 생성합니다. "/course" 경로에 대한 라우터로 태그는 "course"로 설정됩니다.
router = fastapi_utils.CustomAPIRouter(prefix="/course", tags=["course"])

# GET 요청에 사용되는 데이터 모델인 GetRequest를 정의합니다.
class GetRequest(BaseModel):
    cursor: Optional[str] = None  # 선택적인 cursor 파라미터, 기본값은 None입니다.
    count: int = Field(ge=1, le=20)  # count 파라미터, 최소값 1, 최대값 20으로 제한됩니다.

# GET 요청에 대한 응답 데이터 모델인 GetResponse를 정의합니다.
class GetResponse(BaseModel):
    # Course 내부 모델을 정의합니다.
    class Course(BaseModel):
        id: int
        title: str
        created_datetime: datetime.datetime

    # Course 모델의 리스트와 선택적인 next_cursor 값을 가지는 데이터 모델입니다.
    data: list[Course]
    next_cursor: Optional[str]

# 라우터의 api_wrapper 데코레이터를 사용하여 GET 요청 핸들러를 정의합니다.
@router.api_wrapper("GET", "")
async def _(
        q: GetRequest = Depends(),
) -> GetResponse:
    # 초기 cursor_datetime과 cursor_id를 설정합니다.
    cursor_datetime, cursor_id = datetime.datetime.min, 0

    # 만약 q.cursor 값이 존재하면, 해당 값을 사용하여 cursor_datetime과 cursor_id를 업데이트합니다.
    if q.cursor:
        cursor_datetime_str, cursor_id_str = q.cursor.split(',')
        cursor_datetime = datetime.datetime.fromisoformat(cursor_datetime_str)
        cursor_id = int(cursor_id_str)

    # 데이터베이스에서 쿼리를 실행하여 코스 정보를 가져옵니다.
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

    # 다음 페이지를 위한 cursor 값을 계산합니다.
    next_cursor = None
    if courses:
        next_cursor = f"{courses[-1].created_datetime.isoformat()},{courses[-1].id}"

    # GetResponse 모델을 사용하여 결과를 반환합니다.
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


# import datetime

# import sqlalchemy as sa
# from fastapi import Depends
# from pydantic import BaseModel, Field

# from app.utils import fastapi as fastapi_utils
# from app.utils.sqla import db_execute
# from typing import Optional, Tuple

# router = fastapi_utils.CustomAPIRouter(prefix="/course", tags=["course"])


# class GetRequest(BaseModel):
#     cursor: Optional[str] = None
#     count: int = Field(ge=1, le=20)


# class GetResponse(BaseModel):
#     class Course(BaseModel):
#         id: int
#         title: str
#         created_datetime: datetime.datetime

#     data: list[Course]
#     next_cursor: Optional[str]


# @router.api_wrapper(
#     "GET",
#     "",
# )
# async def _(
#         q: GetRequest = Depends(),
# ) -> GetResponse:
#     cursor_datetime, cursor_id = datetime.datetime.min, 0
#     if q.cursor:
#         cursor_datetime_str, cursor_id_str = q.cursor.split(',')
#         cursor_datetime = datetime.datetime.fromisoformat(cursor_datetime_str)
#         cursor_id = int(cursor_id_str)
#     courses = (
#         (
#             await db_execute(
#                 '''
#                 SELECT id, title, created_datetime
#                 FROM course
#                 WHERE (created_datetime, id) > (:cursor_datetime, :cursor_id)
#                 ORDER BY created_datetime ASC, id ASC
#                 LIMIT :count
#                 ''',
#                 {
#                     "cursor_datetime": cursor_datetime,
#                     "cursor_id": cursor_id,
#                     "count": q.count,
#                 },
#             )
#         )
#             .fetchall()
#     )
#     next_cursor = None
#     if courses:
#         next_cursor = f"{courses[-1].created_datetime.isoformat()},{courses[-1].id}"

#     return GetResponse(
#         data=[
#             GetResponse.Course(
#                 id=course.id,
#                 title=course.title,
#                 created_datetime=course.created_datetime,
#             )
#             for course in courses
#         ],
#         next_cursor=next_cursor,
#     )