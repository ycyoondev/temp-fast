-- 사용자 추가
INSERT INTO users (name, email) VALUES ('John Doe', 'john.doe@example.com');

-- 반환된 ID 확인
SELECT * FROM users WHERE name = 'John Doe';

-- 모든 사용자 조회
SELECT * FROM users;

-- 특정 사용자 조회 (예: ID가 1인 사용자)
SELECT * FROM users WHERE id = 1;

-- 사용자 정보 업데이트 (예: ID가 1인 사용자의 이메일 업데이트)
UPDATE users SET email = 'updated.email@example.com' WHERE id = 1;

-- 업데이트된 정보 확인
SELECT * FROM users WHERE id = 1;

-- 사용자 삭제 (예: ID가 1인 사용자 삭제)
DELETE FROM users WHERE id = 1;

-- 삭제 후 확인 (사용자 조회)
SELECT * FROM users;
