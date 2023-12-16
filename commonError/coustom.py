from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# 커스텀 예외 클래스 정의
class ItemNotFoundException(HTTPException):
    def __init__(self, item_id: int):
        # 상태 코드와 에러 메시지 설정
        detail = f"Item with id {item_id} not found"
        super().__init__(status_code=404, detail=detail)

app = FastAPI()

# 공통적인 404 에러를 처리하는 핸들러
@app.exception_handler(ItemNotFoundException)
async def item_not_found_exception_handler(request, exc: ItemNotFoundException):
    # 커스텀 예외 처리
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# 예시적인 라우터
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 42:
        # 예외적인 경우: 커스텀 예외 발생
        raise ItemNotFoundException(item_id)
    else:
        # 정상적인 경우: 해당 아이템의 정보를 반환
        return {"item_id": item_id, "message": "Item found"}
"""
이 코드에서 ItemNotFoundException은 HTTPException을 상속받아 만들어진 커스텀 예외 클래스입니다. 이 클래스를 사용하여 특정 조건에서 404 Not Found 예외를 발생시킵니다. 그리고 해당 예외를 처리하는 핸들러 item_not_found_exception_handler에서는 클라이언트에게 커스텀한 에러 응답을 반환합니다.

이러한 방식을 통해 FastAPI 애플리케이션에서 커스텀 예외를 만들어 사용할 수 있습니다. 이는 응용 프로그램의 특정한 상황에 대한 예외를 정의하고, 그에 따른 처리를 중앙에서 관리하는 데에 유용합니다.
"""