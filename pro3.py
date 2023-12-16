"""
Knapsack dp 적절하게 풀어야함
1. 포션수 = 위장 : 다마심
2. 포션수 > 위장 : DP 만들어가며 마심
3. 큰포션 기준 정렬 후 위장만큼 먹어도 x 암됨 : -1
"""


def solv():
    dp = [[0] * 51 for __ in range(51000)]  # dp[hp회복량][포션수] = mp회복량
    store = []
    n, m, x = map(int, input().split())  # 포션수, 위장, 최소조건
    for _ in range(n):
        a, b = map(int, input().split())
        store.append([a, b])

    store.sort(key=lambda xx: -xx[0])
    # 3번 조건 검사
    temp = 0
    for i in range(m):
        temp += store[i][0]
    if temp < x:
        return -1
    # 1번 조건 검사
    if len(store) == m:
        return sum(aa[1] for aa in store)
    return 0

print(solv())
