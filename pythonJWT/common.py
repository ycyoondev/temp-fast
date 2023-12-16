from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

# FastAPI 애플리케이션 생성
app = FastAPI()

# JWT 설정
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 사용자 정보를 저장할 데이터베이스 대신 간단한 딕셔너리 사용 (실제 프로덕션에서는 데이터베이스 사용 권장)
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": "$2b$12$ik3.WFQ6LF5WmI8XnvG7tOyXj9LBjEmrLR.vsyMz8QuyX3oKg84Ry",  # hashed password for "testpassword"
    }
}

# 패스워드 해싱을 위한 클래스
class PasswordHash:
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer 클래스를 사용하여 토큰을 추출하기 위한 의존성 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 토큰을 생성하는 함수
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 토큰을 검증하고 사용자 정보를 반환하는 함수
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = {"sub": username}
    except JWTError:
        raise credentials_exception
    return token_data

# 토큰 발급을 위한 라우터
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends()):
    user = fake_users_db.get(form_data.username)
    if user and pwd_context.verify(form_data.password, user["password"]):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

# 토큰을 사용한 보호된 라우터
@app.get("/protected-route")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "You have access to this protected route!", "user": current_user}

"""
이 코드에서는 /token 엔드포인트를 통해 로그인을 수행하고, 발급된 토큰을 사용하여 /protected-route 엔드포인트에 접근하는 간단한 예시를 보여줍니다. 패스워드는 해시화하여 저장하고, 토큰은 HS256 알고리즘을 사용하여 서명합니다. 로그인 시에는 사용자 정보와 만료 시간 등을 토큰에 포함하고, /protected-route 엔드포인트에 접근할 때는 get_current_user 함수를 사용하여 토큰을 검증하고 사용자 정보를 추출
"""
