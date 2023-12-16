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

# 라우터에서 데이터 가져오는 함수
@app.get("/get-top-10-users/")
async def get_top_10_users(offset: int = 0, db: Session = Depends(get_db)):
    try:
        # 정렬 후 상위 10개의 데이터 조회
        query = select(User).order_by(User.id).offset(offset).limit(10)
        result = db.execute(query)
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

"""
이 코드에서는 get_top_10_users 함수에서 offset을 사용하여 데이터를 정렬한 후 상위 10개의 데이터를 조회합니다. select(User).order_by(User.id)를 통해 User 테이블을 id 기준으로 정렬하고, offset과 limit을 사용하여 원하는 범위의 데이터를 가져옵니다.

실제로 사용하는 데이터베이스와 테이블에 따라 코드를 수정해야 합니다. 또한, 이 코드는 예시이며, 실제로는 보안과 성능을 고려하여 비밀번호와 연결 문자열 등을 안전하게 관리해야 합니다.
"""

# from fastapi import FastAPI, Depends, HTTPException
# from psycopg2 import connect, sql

# # PostgreSQL 연결 정보
# DATABASE_URL = "postgresql://username:password@localhost/dbname"

# # FastAPI 애플리케이션 생성
# app = FastAPI()

# # 데이터베이스 연결 함수
# def get_db():
#     db = connect(DATABASE_URL)
#     return db

# # 라우터에서 데이터 가져오는 함수
# @app.get("/get-top-10-users/")
# async def get_top_10_users(offset: int = 0, db=Depends(get_db)):
#     try:
#         # 직접 쿼리 문자열 작성
#         query = sql.SQL("SELECT id, name, email FROM users ORDER BY id OFFSET {} LIMIT 10").format(sql.Literal(offset))
        
#         # 쿼리 실행
#         with db.cursor() as cursor:
#             cursor.execute(query)
#             result = cursor.fetchall()
        
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
#     finally:
#         db.close()
