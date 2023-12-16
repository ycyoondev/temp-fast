-- inner
-- users 테이블과 orders 테이블을 user_id로 INNER JOIN
SELECT users.id, users.name, orders.order_number
FROM users
INNER JOIN orders ON users.id = orders.user_id;


-- left join
-- users 테이블과 orders 테이블을 user_id로 LEFT JOIN
SELECT users.id, users.name, orders.order_number
FROM users
LEFT JOIN orders ON users.id = orders.user_id;

-- 3
-- users, orders, products 세 개의 테이블을 조인하는 쿼리
SELECT users.id AS user_id, users.name AS user_name,
       orders.order_number, products.product_name
FROM users
INNER JOIN orders ON users.id = orders.user_id
INNER JOIN products ON orders.product_id = products.id;
