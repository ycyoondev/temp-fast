# main.py

from fastapi import FastAPI, Depends, HTTPException
import httpx

app = FastAPI()

# 의존성: 비동기 HTTP 클라이언트 생성
async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client

# 라우터에서 비동기 함수를 사용하여 데이터 가져오는 함수
@app.get("/get-data/")
async def get_data(http_client: httpx.AsyncClient = Depends(get_http_client)):
    try:
        # 비동기 HTTP 요청을 통해 데이터 가져오기
        response = await http_client.get("https://jsonplaceholder.typicode.com/todos/1")
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리

        data = response.json()
        return data
    except httpx.HTTPError as e:
        # HTTP 오류 처리
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP Error: {str(e)}")
    except Exception as e:
        # 기타 예외 처리
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

"""
이 코드에서는 /get-data/ 엔드포인트를 통해 get_data 함수를 호출합니다. 이 함수에서는 httpx.AsyncClient를 사용하여 비동기 HTTP 요청을 보냅니다. 이렇게 하면 여러 요청을 병렬로 처리하여 성능을 향상시킬 수 있습니다.

주의: 위 코드는 예시이며, 실제로는 데이터베이스 조회, 외부 서비스 호출, 파일 I/O 등에서 비동기를 적용하여 성능을 향상시킬 수 있습니다. 사용 사례에 따라 비동기를 적절히 활용하시기 바랍니다.
"""