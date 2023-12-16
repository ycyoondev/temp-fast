from fastapi import FastAPI, HTTPException, status

app = FastAPI()

# 200 OK - 성공적으로 처리된 경우
@app.get("/success")
def success_example():
    return {"message": "Request processed successfully"}

# 201 Created - 새로운 리소스가 성공적으로 생성된 경우
@app.post("/create-resource", status_code=status.HTTP_201_CREATED)
def create_resource():
    return {"message": "Resource created successfully"}

# 204 No Content - 요청이 성공했지만 응답 본문이 없는 경우
@app.delete("/delete-resource", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource():
    # 리소스 삭제 로직 수행
    return None

# 400 Bad Request - 잘못된 요청이 들어온 경우
@app.post("/bad-request")
def bad_request_example():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request: Invalid input")

# 401 Unauthorized - 인증이 필요한 경우
@app.get("/unauthorized")
def unauthorized_example():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized: Authentication required")

# 404 Not Found - 찾을 수 없는 리소스를 요청한 경우
@app.get("/not-found")
def not_found_example():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found: Resource not found")

# 422 Unprocessable Entity - 요청이 유효하지 않은 경우 (예: 입력 데이터가 형식에 맞지 않음)
@app.post("/unprocessable-entity")
def unprocessable_entity_example():
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unprocessable Entity: Invalid input data")

# 500 Internal Server Error - 서버에서 예외가 발생한 경우
@app.get("/internal-server-error")
def internal_server_error_example():
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error: Something went wrong on the server")
