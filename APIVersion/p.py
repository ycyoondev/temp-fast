from fastapi import FastAPI, APIRouter

app = FastAPI()

# 각 버전에 따른 라우터를 생성합니다.
router_v1 = APIRouter(prefix="/v1", tags=["v1"])
router_v2 = APIRouter(prefix="/v2", tags=["v2"])

# 버전 1의 라우터
@router_v1.get("/items/")
async def read_items_v1():
    return {"version": "v1", "message": "Read items for version 1"}

# 버전 2의 라우터
@router_v2.get("/items/")
async def read_items_v2():
    return {"version": "v2", "message": "Read items for version 2"}

# 애플리케이션에 라우터를 추가합니다.
app.include_router(router_v1)
app.include_router(router_v2)

"""
이 예시에서 /v1/items/와 /v2/items/의 두 가지 버전이 각각 다른 라우터에 의해 처리되고 있습니다. 클라이언트는 요청 시 경로에 따라 적절한 버전의 엔드포인트에 접근할 수 있습니다.

실행하고 난 후 FastAPI 문서를 확인하면 /docs에서 각 버전의 엔드포인트 및 API 문서를 확인할 수 있습니다.

이러한 방식은 간단하게 API 버전을 관리할 수 있습니다. 더 복잡한 상황에서는 헤더를 사용하여 버전을 전달하거나, 별도의 모듈을 사용하여 동적으로 API 버전을 처리하는 방법 등이 고려될 수 있습니다.
"""