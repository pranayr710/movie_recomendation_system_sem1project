import json

# Load JSON data from the file
def load_movie_data(json_file_path='movies_data.json'):
    """Loads movie data from a JSON file."""
    with open(json_file_path, 'r') as file:
        movies = json.load(file)
    return movies

def get_input(prompt, cast_type=str, is_list=False):
    """Generic input handler with casting and optional list processing."""
    user_input = input(prompt).strip()
    if not user_input:
        return None
    if is_list:
        return [cast_type(item.strip().lower()) for item in user_input.split(',')]
    return cast_type(user_input)

def filter_movies(movie_data, genres=None, heroes=None, min_imdb_rating=None, max_imdb_rating=None, min_release_year=None, max_release_year=None, rating=None):
    """Filters movie_data based on provided parameters."""
    found_movies = False
    for movie in movie_data:
        if (
            (genres is None or any(genre in movie["Genre"].lower() for genre in genres)) and
            (heroes is None or any(hero in movie["Hero"].lower() for hero in heroes)) and
            (min_imdb_rating is None or min_imdb_rating <= movie["IMDb Rating"]) and
            (max_imdb_rating is None or movie["IMDb Rating"] <= max_imdb_rating) and
            (min_release_year is None or min_release_year <= movie["Release Year"]) and
            (max_release_year is None or movie["Release Year"] <= max_release_year) and
            (rating is None or rating == movie["Rating"])
        ):
            print(f'Movie found: {movie["Title"]}')
            found_movies = True

    if not found_movies:
        print("No movie found with the provided details.")

# Collect inputs
genres = get_input("Enter genres (comma-separated, leave empty if not applicable): ", is_list=True)
heroes = get_input("Enter heroes (comma-separated, leave empty if not applicable): ", is_list=True)
min_imdb_rating = get_input("Enter minimum IMDb rating (leave empty if not applicable): ", float)
max_imdb_rating = get_input("Enter maximum IMDb rating (leave empty if not applicable): ", float)
min_release_year = get_input("Enter minimum release year (leave empty if not applicable): ", int)
max_release_year = get_input("Enter maximum release year (leave empty if not applicable): ", int)
rating = get_input("Enter rating (leave empty if not applicable): ", float)

# Sample movie data for testing
movie_data = [
    {"Title": "Sample Movie 1", "Genre": "action", "Hero": "Hero A", "IMDb Rating": 7.5, "Release Year": 2020, "Rating": "PG-13"},
    {"Title": "Sample Movie 2", "Genre": "comedy", "Hero": "Hero B", "IMDb Rating": 6.0, "Release Year": 2018, "Rating": "R"},
    # Add more movies as needed for testing
]

# Search for movies based on input criteria
filter_movies(movie_data, genres, heroes, min_imdb_rating, max_imdb_rating, min_release_year, max_release_year, rating)
