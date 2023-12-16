# main.py

from fastapi import FastAPI, HTTPException, Depends
import httpx

app = FastAPI()

# 외부 API 엔드포인트
EXTERNAL_API_URL = "https://jsonplaceholder.typicode.com/todos/1"

# 비동기 HTTP 클라이언트 생성
async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client

# 비동기 함수를 사용하여 외부 API를 호출하는 함수
async def call_external_api(http_client: httpx.AsyncClient = Depends(get_http_client)):
    try:
        # 비동기 HTTP 요청을 통해 외부 API 호출
        response = await http_client.get(EXTERNAL_API_URL)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        data = response.json()
        return data
    except httpx.HTTPError as e:
        # HTTP 오류 처리
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP Error: {str(e)}")
    except Exception as e:
        # 기타 예외 처리
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# 외부 API 호출을 위한 라우터
@app.get("/call-external-api/")
async def get_external_data(data: dict = Depends(call_external_api)):
    return data
"""
이 코드에서는 /call-external-api/ 엔드포인트를 통해 get_external_data 함수를 호출합니다. 이 함수에서는 httpx.AsyncClient를 사용하여 비동기 HTTP 요청을 통해 외부 API를 호출합니다.

주의: 실제로 사용할 때는 호출하려는 외부 API의 엔드포인트와 요청 방식, 필요한 헤더 등을 확인하여 코드를 수정해야 합니다. 또한, 비동기적으로 외부 API를 호출할 때에는 호출되는 외부 API가 비동기를 지원하는지 확인하는 것이 중요합니다.
"""
