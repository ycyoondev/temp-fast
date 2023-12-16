# pip install fastapi[all] psycopg2-binary

# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# PostgreSQL 연결 설정
DATABASE_URL = "postgresql+psycopg2://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# 모델 정의 (예: User 테이블)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

# 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 애플리케이션 생성
app = FastAPI()

# Dependency: 데이터베이스 세션
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# 라우터에서 페이지네이션을 적용하여 데이터 가져오는 함수
@app.get("/get-users/")
async def get_users(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        # 페이지네이션을 적용한 데이터 조회
        query = select(User).order_by(User.id).offset(offset).limit(limit)
        result = db.execute(query)
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

"""
이 코드에서는 /get-users/ 엔드포인트를 통해 get_users 함수를 호출합니다. 이 함수에서는 offset과 limit을 사용하여 페이지네이션을 적용하여 데이터를 조회합니다. select(User).order_by(User.id)를 통해 User 테이블을 id를 기준으로 정렬하고, offset과 limit을 사용하여 원하는 범위의 데이터를 가져옵니다.
"""