# pip install cachetools

from fastapi import FastAPI, Depends
from functools import lru_cache
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from cachetools import LRUCache, cached

# SQLAlchemy 모델 정의
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# 데이터베이스 연결 문자열
DATABASE_URL = "sqlite:///./test.db"

# 데이터베이스 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 생성 함수
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# FastAPI 애플리케이션 생성
app = FastAPI()

# 캐시 설정
cache = LRUCache(maxsize=128)

# 캐시된 함수 정의
@cached(cache)
def get_items_from_db(db: Session, start: int = 0, limit: int = 10):
    # DB에서 아이템 조회
    query = select(Item).offset(start).limit(limit)
    items = db.execute(query).scalars().all()
    return items

# 라우터에서 캐시된 함수를 호출하여 조회 성능을 높임
@app.get("/cached-items/")
async def read_cached_items(start: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # 캐시된 함수 호출
    items = get_items_from_db(db, start=start, limit=limit)

    # 결과 반환
    return {"items": [{"id": item.id, "name": item.name} for item in items]}

"""
이 코드에서는 cachetools.LRUCache를 사용하여 LRU(Least Recently Used) 캐시를 설정했습니다. @cached(cache) 데코레이터를 사용하여 함수에 캐시를 적용하고, 함수의 인자를 기반으로 캐시 키를 생성합니다. 함수가 호출될 때 캐시된 결과가 반환되므로, 동일한 매개변수로 함수를 호출할 때는 DB에 다시 쿼리를 날리지 않고 캐시된 결과가 사용됩니다.
"""