from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
import datetime

# SQLAlchemy 모델을 정의합니다.
Base = declarative_base()

class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    created_datetime = Column(DateTime, default=func.now())

# 데이터베이스 연결 문자열을 설정합니다.
DATABASE_URL = "sqlite:///./test.db"

# 데이터베이스 엔진을 생성합니다.
engine = create_engine(DATABASE_URL)

# 세션 생성기를 생성합니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI 애플리케이션을 생성합니다.
app = FastAPI()

# GET 요청 핸들러를 정의합니다.
@app.get("/courses/")
async def get_courses(cursor: Optional[datetime.datetime] = None, count: int = 10):
    # 데이터베이스 세션을 가져옵니다.
    db = SessionLocal()

    try:
        # cursor 값이 주어졌을 때, 해당 시간 이후의 데이터만 조회합니다.
        if cursor:
            courses = db.query(Course).filter(Course.created_datetime > cursor).limit(count).all()
        else:
            # cursor 값이 주어지지 않았을 때, 처음부터 count 개수만큼의 데이터를 조회합니다.
            courses = db.query(Course).limit(count).all()

        # 다음 페이지를 위한 cursor 값을 계산합니다.
        next_cursor = None
        if courses:
            next_cursor = courses[-1].created_datetime

        return {"data": courses, "next_cursor": next_cursor}

    finally:
        # 세션을 닫습니다.
        db.close()
