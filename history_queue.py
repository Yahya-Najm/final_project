from collections import deque


class ViewingHistory:
    # FIFO queue capped at max_size; oldest entry is auto-dropped when full
    def __init__(self, max_size=5):
        self._queue = deque(maxlen=max_size)

    def add(self, movie_id):
        self._queue.append(movie_id)

    def get_history(self):
        # Returns list ordered from oldest to newest
        return list(self._queue)

    def is_empty(self):
        return len(self._queue) == 0

    def __contains__(self, movie_id):
        return movie_id in self._queue

    def __len__(self):
        return len(self._queue)
