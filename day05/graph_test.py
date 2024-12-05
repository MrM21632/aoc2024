import collections


graph = {
    47: [53, 13, 61, 29],
    97: [13, 61, 47, 29, 53, 75],
    75: [29, 53, 47, 61, 13],
    61: [13, 53, 29],
    29: [13],
    53: [29, 13],
    13: [],
}

indegree = {
    13: 6,
    29: 5,
    47: 2,
    53: 4,
    61: 3,
    75: 1,
    97: 0,
}

queue = collections.deque([i for i in indegree.keys() if indegree[i] == 0])
visited = 0
while queue:
    curr = queue.popleft()
    visited += 1
    for neighbor in graph[curr]:
        indegree[neighbor] -= 1
        if indegree[neighbor] == 0:
            queue.append(neighbor)

print(visited == len(indegree.keys()))
