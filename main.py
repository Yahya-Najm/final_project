from dataset import initial_movies
from hash_tables import MovieRegistry, UserRatings
from history_queue import ViewingHistory
from graph_bfs import MovieGraph


def display_table(movies, registry=None):
    # Prints a formatted table of movie info including avg rating
    print(f"\n{'ID':<5} {'Title':<38} {'Genres':<38} {'Avg Rating'}")
    print("-" * 90)
    for m in movies:
        avg = m["sum_rating"] / m["count"] if m["count"] else 0
        genres = ", ".join(m["genres"])
        print(f"{m['id']:<5} {m['title']:<38} {genres:<38} {avg:.2f}")


def get_int(prompt):
    # Safely reads an integer from the user; returns None on invalid input
    try:
        return int(input(prompt).strip())
    except ValueError:
        return None


def get_float(prompt):
    try:
        return float(input(prompt).strip())
    except ValueError:
        return None


def main():
    registry = MovieRegistry(initial_movies)
    user_ratings = UserRatings()
    history = ViewingHistory(max_size=5)
    graph = MovieGraph(initial_movies)

    menu = (
        "\n--- Movie RecSys ---\n"
        "1. All movies\n"
        "2. Top 5 movies\n"
        "3. Watch a movie\n"
        "4. Rate a watched movie\n"
        "5. Viewing history\n"
        "6. Get recommendations\n"
        "0. Exit\n"
    )

    while True:
        print(menu)
        choice = input("Choice: ").strip()

        if choice == "1":
            display_table(registry.get_all_movies())

        elif choice == "2":
            print("\nTop 5 Movies by Rating:")
            display_table(registry.get_top_n(5))

        elif choice == "3":
            movie_id = get_int("Enter movie ID to watch: ")
            if movie_id is None:
                print("Invalid ID.")
                continue
            movie = registry.get_movie(movie_id)
            if not movie:
                print("Movie not found.")
            else:
                history.add(movie_id)
                print(f"Now watching: {movie['title']}")

        elif choice == "4":
            if history.is_empty():
                print("Watch a movie first.")
                continue
            movie_id = get_int("Enter movie ID to rate: ")
            if movie_id is None:
                print("Invalid ID.")
                continue
            if movie_id not in history:
                print("You can only rate movies you have watched.")
            elif user_ratings.has_rated(movie_id):
                print("You already rated this movie.")
            else:
                score = get_float("Score (1-10): ")
                if score is None or not (1 <= score <= 10):
                    print("Score must be a number between 1 and 10.")
                else:
                    user_ratings.rate(movie_id, score)
                    registry.update_rating(movie_id, score)
                    print(f"Rating saved. New avg: {registry.get_avg_rating(movie_id)}")

        elif choice == "5":
            hist = history.get_history()
            if not hist:
                print("No viewing history yet.")
            else:
                print("\nLast watched (oldest to newest):")
                for mid in hist:
                    movie = registry.get_movie(mid)
                    print(f"  [{mid}] {movie['title']}")

        elif choice == "6":
            hist = history.get_history()
            if not hist:
                print("Watch some movies first to get recommendations.")
            else:
                viewed = set(hist)
                recs = graph.bfs_recommend(hist, registry, viewed)
                if recs:
                    print("\nRecommended for you:")
                    display_table(recs)
                else:
                    print("No recommendations found. Try watching more movies.")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 0-6.")


if __name__ == "__main__":
    main()
