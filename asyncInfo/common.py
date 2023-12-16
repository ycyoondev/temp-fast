from fastapi import FastAPI
import time
import asyncio

app = FastAPI()

# 동기적으로 실행하는 예시
@app.get("/sync")
def sync_endpoint():
    # 현재 시각을 출력하고 1초 대기하는 동기적인 코드
    print("Sync Endpoint Start")
    time.sleep(1)
    print("Sync Endpoint End")
    return {"message": "Sync Endpoint Completed"}

# 비동기적으로 실행하는 예시
@app.get("/async")
async def async_endpoint():
    # 현재 시각을 출력하고 1초 대기하는 비동기적인 코드
    print("Async Endpoint Start")
    await asyncio.sleep(1)
    print("Async Endpoint End")
    return {"message": "Async Endpoint Completed"}
"""
동기 코드 (sync_endpoint):
time.sleep(1)은 현재 스레드를 1초 동안 대기시킵니다.
이 시간 동안 다른 요청을 처리하지 못하고 대기합니다.

비동기 코드 (async_endpoint):
await asyncio.sleep(1)은 현재 실행 중인 함수를 일시 중단하고 다른 작업을 처리한 후, 1초 후에 다시 해당 함수를 실행합니다.
이렇게 비동기로 작성된 함수는 다른 작업이 수행되는 동안 블로킹되지 않고 다른 작업을 처리할 수 있습니다.
동기 코드의 경우 한 번에 하나의 요청만을 처리하고 대기하는 동안 다른 요청을 처리하지 않습니다. 반면에 비동기 코드는 여러 작업을 동시에 처리할 수 있어서 동시성이 높아집니다. 특히 I/O 바운드 작업이 많은 상황에서 비동기 코드를 사용하면 성능 향상을 기대할 수 있습니다.

"""