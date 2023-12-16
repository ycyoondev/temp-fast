# pip install aiohttp

# main.py

from fastapi import FastAPI, HTTPException, Depends
import aiohttp

app = FastAPI()

# 외부 API 엔드포인트
EXTERNAL_API_URL = "https://jsonplaceholder.typicode.com/todos/1"

# 비동기 HTTP 클라이언트 설정
async def get_http_client():
    async with aiohttp.ClientSession() as client:
        yield client

# 외부 API를 비동기적으로 호출하는 함수
async def call_external_api(http_client: aiohttp.ClientSession = Depends(get_http_client)):
    try:
        # 비동기 HTTP 요청을 사용하여 외부 API 호출
        async with http_client.get(EXTERNAL_API_URL) as response:
            response.raise_for_status()  # HTTP 오류 시 예외 처리

            data = await response.json()
            return data
    except aiohttp.ClientResponseError as e:
        # HTTP 오류 처리
        raise HTTPException(status_code=e.status, detail=f"HTTP 오류: {str(e)}")
    except Exception as e:
        # 기타 예외 처리
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")

# 외부 API 호출을 위한 라우터
@app.get("/call-external-api/")
async def get_external_data(data: dict = Depends(call_external_api)):
    return data

"""
이 예시에서는 /call-external-api/ 엔드포인트가 get_external_data 함수를 호출하며, 해당 함수에서는 aiohttp.ClientSession을 사용하여 비동기 HTTP 요청을 통해 지정된 외부 API 엔드포인트를 호출합니다.
"""