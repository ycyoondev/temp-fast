from fastapi import FastAPI, HTTPException

app = FastAPI()

# 공통적인 404 에러를 처리하는 핸들러
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# 공통적인 500 에러를 처리하는 핸들러
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )

# 예시적인 라우터
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 42:
        # 예외적인 경우: 특정 조건에서 404 Not Found 반환
        raise HTTPException(status_code=404, detail="Item not found")
    elif item_id == 0:
        # 예외적인 경우: 특정 조건에서 500 Internal Server Error 반환
        raise Exception("Something went wrong")
    else:
        # 정상적인 경우: 해당 아이템의 정보를 반환
        return {"item_id": item_id, "message": "Item found"}

"""
이 예시에서 http_exception_handler 함수는 HTTPException이 발생할 때 호출되며, generic_exception_handler 함수는 모든 다른 예외(Exception 클래스를 상속받은 예외)가 발생할 때 호출됩니다.

HTTPException 클래스는 FastAPI에서 예외를 처리할 때 사용되며, 해당 예외를 발생시키면 FastAPI는 등록된 핸들러에게 해당 예외를 전달합니다. 이를 통해 중앙집중식으로 에러를 처리하고 클라이언트에게 일관된 에러 응답을 제공할 수 있습니다.

더 복잡한 상황에서는 커스텀 예외를 만들어 사용하거나, HTTPException을 더 세밀하게 활용하여 상태 코드, 메시지 등을 조절할 수 있습니다.
"""