# app/utils/misc.py

from fastapi import Depends, HTTPException
from aioredis import Redis, create_redis_pool

async def get_redis() -> Redis:
    redis = await create_redis_pool("redis://localhost:6379/0")
    return redis

# main.py

from fastapi import FastAPI, Depends
from app.utils.misc import get_redis
from aioredis import Redis

app = FastAPI()

# 데이터를 저장하고 캐시된 데이터를 조회하는 함수
async def process_data(db_data: str, redis: Redis = Depends(get_redis)) -> str:
    # 데이터를 Redis에 저장 (실제 상황에서는 DB에서 가져온 데이터를 여기에서 사용)
    await redis.setex("cached_key", 60, db_data)
    
    # 캐시된 데이터를 조회
    cached_data = await redis.get("cached_key")
    if cached_data:
        return cached_data.decode("utf-8")
    else:
        return "Fallback data"  # 캐시된 데이터가 없을 경우 대체 데이터 사용

# 라우터에서 데이터 처리 함수 호출
@app.get("/process-data")
async def read_processed_data(processed_data: str = Depends(process_data)):
    return {"processed_data": processed_data}

"""
이 코드에서는 /process-data 엔드포인트를 통해 process_data 함수를 호출합니다. 이 함수는 get_redis 함수를 사용하여 Redis에 데이터를 저장하고, 캐시된 데이터를 조회합니다. 만약 캐시된 데이터가 없으면 대체 데이터를 반환합니다.

이렇게 함으로써 get_redis 함수를 이용하여 Redis를 활용하는 코드를 모듈화하고, 데이터를 저장하고 캐시된 데이터를 조회하여 성능을 향상시킬 수 있습니다.
"""