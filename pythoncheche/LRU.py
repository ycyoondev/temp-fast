from fastapi import FastAPI
from functools import lru_cache

app = FastAPI()

# 캐시할 함수 정의
@lru_cache(maxsize=128)  # maxsize는 캐시 크기를 의미하며, 적절한 크기를 선택하세요.
def expensive_query(param: int) -> str:
    # 여기에서는 가정상의 비용이 큰 쿼리를 시뮬레이션
    print(f"Executing expensive query for param: {param}")
    return f"Result for param {param}"

# 라우터에서 캐시된 함수를 호출하여 조회 성능을 높임
@app.get("/cached-query/{param}")
async def read_cached_query(param: int):
    result = expensive_query(param)
    return {"result": result}

"""
이 코드에서 expensive_query 함수는 캐시를 사용하여 결과를 저장하고, @lru_cache 데코레이터를 통해 캐시 크기를 설정합니다. 이 함수는 매개변수 param에 따라 다양한 비용이 큰 작업을 시뮬레이션하는 함수입니다.

라우터에서는 이 함수를 호출하여 캐시된 결과를 반환합니다. 첫 번째 호출에서는 비용이 큰 작업이 실행되지만, 그 이후의 호출에서는 이전에 캐시된 결과가 반환되므로 조회 성능이 향상됩니다.

캐시를 사용하는 것은 특히 반복적으로 실행되는 작업이 있을 때 유용하며, 결과가 자주 변경되지 않는 경우에 적합합니다.


캐시를 저장하고 사용하는 주요 단계는 다음과 같습니다:

캐시할 함수 정의: expensive_query 함수는 @lru_cache 데코레이터를 사용하여 캐시를 적용한 함수입니다. 이 함수는 비용이 큰 작업을 시뮬레이션하며, 결과가 캐시에 저장됩니다.

라우터에서 캐시된 함수 호출: read_cached_query 라우터에서는 캐시된 함수를 호출하여 결과를 얻습니다. 첫 번째 호출에서는 실제로 비용이 큰 작업이 실행되고 결과가 캐시에 저장됩니다.

결과 반환: 캐시된 함수의 결과를 반환하여 성능을 향상시킵니다. 이후 동일한 매개변수로 함수를 호출하면 이전에 캐시된 결과가 반환됩니다.

캐시의 크기(maxsize)를 적절하게 조절하여 메모리 사용량을 관리할 수 있습니다. 또한, 캐시를 사용할 때 주의할 점은 캐시된 결과가 메모리에 저장되므로, 메모리 사용량이 큰 경우에는 적절한 설정이 필요합니다.
"""