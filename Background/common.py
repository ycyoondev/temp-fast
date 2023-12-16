from fastapi import FastAPI, BackgroundTasks
from typing import List
import asyncio

app = FastAPI()

# 비동기적으로 실행되는 작업 함수
async def async_task(item: int):
    await asyncio.sleep(1)
    print(f"Processing item {item}")

# 동시에 실행되는 작업을 처리할 함수
async def process_items_async(items: List[int]):
    # 비동기 함수로 각 아이템을 처리
    await asyncio.gather(*(async_task(item) for item in items))

# 라우터에서 비동기 함수를 호출하고 백그라운드 작업 실행
@app.post("/process-items/")
async def process_items(items: List[int], background_tasks: BackgroundTasks):
    # 백그라운드 작업을 FastAPI의 BackgroundTasks를 통해 등록
    background_tasks.add_task(process_items_async, items)
    return {"message": "Processing items in the background"}

"""
이 코드에서 async_task 함수는 비동기적으로 실행되는 작업을 나타냅니다. 그리고 process_items_async 함수는 받은 아이템 리스트를 비동기 함수를 통해 동시에 처리합니다. 라우터에서는 BackgroundTasks를 사용하여 백그라운드 작업을 등록하고, 비동기 함수를 실행시킵니다.

이렇게 비동기 함수를 사용하면 동시성을 확보하면서도 블로킹되는 부분이 없어서 효율적으로 작업을 처리할 수 있습니다.
"""