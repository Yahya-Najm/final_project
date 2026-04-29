from collections import deque


class MovieGraph:
    # Adjacency list graph where edges connect movies that share at least one genre
    def __init__(self, movies):
        self._graph = {}
        self._build(movies)

    def _build(self, movies):
        movie_list = list(movies.values())
        for m in movie_list:
            self._graph[m["id"]] = set()

        # Compare every pair once; add bidirectional edge if genres overlap
        for i in range(len(movie_list)):
            for j in range(i + 1, len(movie_list)):
                m1, m2 = movie_list[i], movie_list[j]
                if set(m1["genres"]) & set(m2["genres"]):
                    self._graph[m1["id"]].add(m2["id"])
                    self._graph[m2["id"]].add(m1["id"])

    def bfs_recommend(self, start_ids, registry, viewed_ids, top_n=5):
        # BFS from all seed nodes; collects unvisited, unwatched neighbors as candidates
        visited = set(start_ids)
        queue = deque(start_ids)
        candidates = []

        while queue:
            current = queue.popleft()
            for neighbor in self._graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    if neighbor not in viewed_ids:
                        movie = registry.get_movie(neighbor)
                        if movie and movie["count"] > 0:
                            avg = movie["sum_rating"] / movie["count"]
                            candidates.append((avg, movie))

        # Sort by avg rating so best recommendations come first
        candidates.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in candidates[:top_n]]
