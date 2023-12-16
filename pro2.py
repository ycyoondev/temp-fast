"""
1, 2는 lazy하게 하자

"""
import math
from collections import deque

fact = [1 for _ in range(500000 + 1)]
p = 1000000007
calced_n = 0

def pow(a, b):
    if b == 0:
        return 1
    mid = pow(a, b // 2)

    if b % 2 == 0:
        return mid * mid % p
    else:
        return a * mid * mid % p

def ncr(n, k): # n >= k
    global fact, calced_n
    if calced_n < n+1:
        for i in range(2, n + 1):
            fact[i] = (fact[i-1] * i) % p
        calced_n = n+1

    t_1 = fact[n] % p
    t_2 = pow(fact[k] * fact[n-k] % p, p-2) % p
    return t_1 * t_2 % p

x = 0
n = 0
r = 0

dq = deque()


def solv():
    global n, r, x

    n, r, q = map(int, input().split())

    for _ in range(q):
        qry = list(map(int, input().split()))
        if qry[0] in (1, 2):
            dq.appendleft((qry[0], qry[1]))
        else:
            while dq:
                a, b = dq.pop()
                if a == 1:
                    n += b
                else:
                    r += b
            if r > n:
                continue
            # p = math.factorial(n) // (math.factorial(r) * math.factorial(n-r))
            p = ncr(n, r)
            x = x ^ p
    return x

print(solv())

"""
import math
from collections import deque

x = 0
n = 0
r = 0

dq = deque()


def solv():
    global n, r, x

    n, r, q = map(int, input().split())

    for _ in range(q):
        qry = list(map(int, input().split()))
        if qry[0] in (1, 2):
            dq.appendleft((qry[0], qry[1]))
        else:
            while dq:
                a, b = dq.pop()
                if a == 1:
                    n += b
                else:
                    r += b
            if r > n:
                continue
            p = math.factorial(n) // (math.factorial(r) * math.factorial(n-r))
            p = p % 1000000007
            x = x ^ p
    return x
"""

"""
def solv():
    global n, r, x
    n, r, q = map(int, input().split())
    for _ in range(q):
        qry = list(map(int, input().split()))
        if qry[0] == 1:
            n += qry[1]
        elif qry[0] == 2:
            r += qry[1]
        else:
            if r > n:
                continue
            p = math.factorial(n) // (math.factorial(r) * math.factorial(n-r))
            p = p % 1000000007
            x = x ^ p
    return x
"""