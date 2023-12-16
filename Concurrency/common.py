from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
import datetime

# SQLAlchemy 모델 정의
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())

# 데이터베이스 연결 문자열
DATABASE_URL = "sqlite:///./test.db"

# 데이터베이스 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 생성기 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# 공통적인 500 에러를 처리하는 핸들러
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )

# 비동기적으로 데이터베이스 쿼리 실행
async def get_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

# 라우터
@app.get("/items/", response_model=List[Item])
async def read_items():
    # 비동기 함수를 Depends로 사용하여 동시성 활용
    items = await Depends(get_items)
    return items
"""
이 코드에서 get_items 함수는 데이터베이스에서 아이템 목록을 가져오는 비동기 함수입니다. Depends를 통해 이 함수를 의존성으로 사용하면 FastAPI는 해당 함수를 비동기적으로 실행하고, 동시에 다른 요청을 처리할 수 있습니다.
"""