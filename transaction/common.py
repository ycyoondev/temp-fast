from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

app = FastAPI()

# PostgreSQL 연결 설정
DATABASE_URL = "postgresql+psycopg2://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 정의 (예: User 테이블)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

# 테이블 생성
Base.metadata.create_all(bind=engine)

# 의존성: 데이터베이스 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 라우터에서 트랜잭션을 사용하여 데이터를 조회하는 함수
@app.get("/get-users/")
def get_users(db: Session = Depends(get_db)):
    try:
        # 트랜잭션 시작
        with db.begin():
            # 데이터베이스 쿼리
            users = db.execute(select(User)).fetchall()
        return users
    except Exception as e:
        # 트랜잭션 롤백 및 예외 처리
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

"""
FastAPI에서 트랜잭션을 관리하는 코드는 주로 데이터베이스와의 상호 작용에서 발생합니다. 아래는 SQLAlchemy를 사용하여 PostgreSQL 데이터베이스에서 트랜잭션을 관리하는 간단한 예시 코드입니다. 코드에서는 Session 객체를 사용하여 트랜잭션을 시작하고 관리합니다.
이 코드에서는 /get-users/ 엔드포인트를 통해 get_users 함수를 호출합니다. 함수 내에서는 SessionLocal을 사용하여 데이터베이스 세션을 생성하고, with db.begin():을 사용하여 트랜잭션을 시작합니다. 데이터베이스 쿼리 후 성공 시 트랜잭션이 커밋되고, 예외가 발생하면 롤백됩니다.
"""