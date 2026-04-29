import copy


class MovieRegistry:
    # Stores all movies in a dict for O(1) lookup, update, and retrieval by ID
    def __init__(self, initial_data):
        self._movies = copy.deepcopy(initial_data)

    def get_movie(self, movie_id):
        return self._movies.get(movie_id)

    def get_all_movies(self):
        return list(self._movies.values())

    def update_rating(self, movie_id, new_score):
        # O(1) avg update: add to running sum and increment count
        movie = self._movies.get(movie_id)
        if movie:
            movie["sum_rating"] += new_score
            movie["count"] += 1

    def get_avg_rating(self, movie_id):
        movie = self._movies.get(movie_id)
        if movie and movie["count"] > 0:
            return round(movie["sum_rating"] / movie["count"], 2)
        return 0.0

    def get_top_n(self, n=5):
        # Sort by avg rating descending, return top n
        rated = [m for m in self._movies.values() if m["count"] > 0]
        return sorted(rated, key=lambda m: m["sum_rating"] / m["count"], reverse=True)[:n]


class UserRatings:
    # Tracks which movies the user has rated and the score given; key = movie_id
    def __init__(self):
        self._ratings = {}

    def rate(self, movie_id, score):
        # Prevents double-voting; returns False if already rated
        if movie_id in self._ratings:
            return False
        self._ratings[movie_id] = score
        return True

    def has_rated(self, movie_id):
        return movie_id in self._ratings

    def get_rated_ids(self):
        return set(self._ratings.keys())
