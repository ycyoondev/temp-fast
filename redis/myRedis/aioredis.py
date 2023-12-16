# pip install aioredis

from fastapi import FastAPI, Depends, HTTPException
from aioredis import create_redis_pool, Redis

app = FastAPI()

# Redis 연결 설정
REDIS_URL = "redis://localhost:6379/0"

# 데이터베이스에서 가져올 가상의 데이터
fake_data = {"user_id": 1, "username": "example_user"}

# Redis 연결 풀 생성
async def get_redis() -> Redis:
    redis = await create_redis_pool(REDIS_URL)
    return redis

# 캐시된 데이터를 조회하는 함수
async def get_cached_data(redis: Redis, key: str) -> str:
    # Redis에서 데이터 조회
    cached_data = await redis.get(key)
    
    if cached_data:
        # 캐시에 데이터가 있으면 반환
        return cached_data.decode("utf-8")
    else:
        # 캐시에 데이터가 없으면 가상의 데이터를 캐시에 저장하고 반환
        await redis.setex(key, 60, "example_data")
        return "example_data"

# 라우터에서 캐시된 데이터를 조회하는 함수
@app.get("/cached-data/{key}")
async def read_cached_data(key: str, redis: Redis = Depends(get_redis)):
    try:
        # 캐시된 데이터를 조회
        cached_data = await get_cached_data(redis, key)
        return {"key": key, "data": cached_data}
    except Exception as e:
        # 예외 처리
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

"""
이 코드에서는 /cached-data/{key} 엔드포인트를 통해 Redis를 사용하여 캐시된 데이터를 조회하는 간단한 예시를 보여줍니다.

get_redis: aioredis를 사용하여 Redis 연결 풀을 생성하는 함수입니다.
get_cached_data: Redis에서 데이터를 조회하고 캐시에 저장하는 함수입니다. 데이터가 캐시에 없는 경우, 가상의 데이터를 캐시에 저장합니다.
/cached-data/{key} 엔드포인트: Redis를 사용하여 캐시된 데이터를 조회하는 라우터입니다. Depends(get_redis)를 사용하여 라우터에서 Redis 연결을 주입합니다.
이러한 방식으로 Redis를 사용하면 데이터베이스 조회 비용을 줄이고 성능을 향상시킬 수 있습니다.
"""