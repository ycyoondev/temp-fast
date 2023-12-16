"""
4 4 v e
1 2 3 # 그래프
2 3 2
2 4 4
3 4 1

"""
def findparent(parent, x):
    if parent[x] != x:
        parent[x] = findparent(parent, parent[x])
    return parent[x]

def unionparent(parent, a, b):
    a = findparent(parent, a)
    b = findparent(parent, b)
    if a < b:
        parent[b] = a
    else:
        parent[a] = b

def solv():
    v, e = map(int, input().split())
    parent = [0] * (v + 1)

    for i in range(1, v + 1):
        parent[i] = i

    edges = []
    result = 0

    for _ in range(e):
        a, b, cost = map(int, input().split())
        edges.append((cost, a, b))

    edges.sort()

    for edge in edges:
        cost, a, b = edge
        if findparent(parent, a) != findparent(parent, b):
            unionparent(parent, a, b)
            result += cost

    return result

'''
[Input Example 1]
7 9
1 2 29
1 5 75
2 3 35
2 6 34
3 4 7
4 6 23
4 7 13
5 6 53
6 7 25
[Output Example 1]
159
'''
print(solv())