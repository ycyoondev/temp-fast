import datetime
import json

import sqlalchemy as sa
from fastapi import Depends
from pydantic import BaseModel

from app.utils import fastapi as fastapi_utils
from app.utils.misc import db_commit, db_execute, get_redis

router = fastapi_utils.CustomAPIRouter(prefix="", tags=[""])


class DashboardGetResponse(BaseModel):
    id: int
    title: str
    article_count: int
    created_datetime: datetime.datetime


@router.api_wrapper(
    "GET",
    "/board/dashboard",
)
async def _() -> list[DashboardGetResponse]:
    redis = await get_redis()
    cached_data = await redis.get('dashboard')
    if cached_data:
        return json.loads(cached_data) # cached 있으면 끝
    boards = (
        (
            await db_execute(
                '''
                SELECT 
                    b.id as id, 
                    b.title as title, 
                    COUNT(ba.id) as cnt, 
                    b.created_datetime as created_datetime
                FROM board b
                LEFT JOIN board_article ba 
                ON b.id = ba.board_id
                GROUP BY b.id, b.title, b.created_datetime
                ORDER BY cnt DESC
                LIMIT 10
                '''
            )
        )
        .fetchall()
    )
    result = [
        DashboardGetResponse(
            id=board.id,
            title=board.title,
            article_count=board.cnt,
            created_datetime=board.created_datetime,
        ).dict()
        for board in boards
    ]
    await redis.set('dashboard', json.dumps(result, default=str), ex=3600) # redis key 생성
    return result



class ArticleCreateRequest(BaseModel):
    board_id: int
    title: str


@router.api_wrapper(
    "POST",
    "/article",
)
async def _(
    q: ArticleCreateRequest,
) -> None:
    await db_execute(
        '''
        INSERT INTO board_article (board_id, title, created_datetime)
        VALUES (:board_id, :title, CURRENT_TIMESTAMP)
        ''',
        {
            "board_id": q.board_id,
            "title": q.title,
        }
    )

    await db_commit()
    await get_redis().delete('dashboard') # key 삭제


@router.api_wrapper(
    "DELETE",
    "/article/{article_id}",
)
async def _(
    article_id: int,
) -> None:
    await db_execute(
        '''
        DELETE FROM board_article
        WHERE id = :article_id
        ''',
        {
            "article_id": article_id,
        }
    )

    await db_commit()
    await get_redis().delete('dashboard') # key 삭제