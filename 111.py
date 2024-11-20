import json
import pandas as pd
import File_handling

json_file_path = 'movies_data.json'

with open(json_file_path, 'r') as json_file:
    movie_data = json.load(json_file)
    
# Load the movie data from the JSON file
json_file_path = 'movies_data.json'


# Load JSON data from the file
def load_movie_data(json_file_path='movies_data.json'):
    """Loads movie data from a JSON file."""
    with open(json_file_path, 'r') as file:
        movies = json.load(file)
    return movies

# Filter movies based on genre
def filter_by_genre(movies, genre):
    """Filters movies by genre."""
    if genre:
        return [movie for movie in movies if genre.lower() in movie.get("Genre", "").lower()]
    return movies

# Filter movies based on IMDb rating range
def filter_by_imdb_rating(movies, imdb_min, imdb_max):
    """Filters movies by minimum and maximum IMDb rating."""
    if imdb_min is not None:
        movies = [movie for movie in movies if movie.get("Imdb") >= imdb_min]
    if imdb_max is not None:
        movies = [movie for movie in movies if movie.get("Imdb") <= imdb_max]
    return movies

# Filter movies based on actor's name
def filter_by_actor(movies, actor):
    """Filters movies by actor's name."""
    if actor:
        return [movie for movie in movies if actor.lower() in movie.get("Actor", "").lower()]
    return movies

# Filter movies based on year range
def filter_by_year_range(movies, start_year, end_year):
    """Filters movies by a range of years."""
    if start_year is not None and end_year is not None:
        return [movie for movie in movies if start_year <= movie.get("Year") <= end_year]
    return movies

# Filter movies based on age certification
def filter_by_age_certification(movies, age_certification):
    """Filters movies by age certification."""
    if age_certification:
        return [movie for movie in movies if movie.get("Age Certification") == age_certification]
    return movies

# Display filtered movie data
def display_movies(movies):
    """Displays a list of movies in a formatted way."""
    if movies:
        for movie in movies:
            print(f"Title: {movie['Title']}, Year: {movie['Year']}, Genre: {movie['Genre']}, "
                  f"Director: {movie['Director']}, Actor: {movie['Actor']}, "
                  f"Age Certification: {movie['Age Certification']}, IMDb: {movie['Imdb']}")
    else:
        print("No movies match the specified criteria.")

# Get filter criteria from the user
def get_user_input():
    """Prompts the user to input filter criteria and returns them."""
    genre = input("Enter the genre (or press Enter to skip): ")
    genre = genre if genre else None
    
    imdb_min = input("Enter minimum IMDb rating (or press Enter to skip): ")
    imdb_min = float(imdb_min) if imdb_min else None
    
    imdb_max = input("Enter maximum IMDb rating (or press Enter to skip): ")
    imdb_max = float(imdb_max) if imdb_max else None
    
    actor = input("Enter the actor's name (or press Enter to skip): ")
    actor = actor if actor else None
    
    start_year = input("Enter the start year (or press Enter to skip): ")
    start_year = int(start_year) if start_year else None
    
    end_year = input("Enter the end year (or press Enter to skip): ")
    end_year = int(end_year) if end_year else None
    
    age_certification = input("Enter age certification (or press Enter to skip): ")
    age_certification = age_certification if age_certification else None
    
    return genre, imdb_min, imdb_max, actor, start_year, end_year, age_certification

# Main function to load data, get input, filter, and display movies
def main():
    """Main function to run the movie filtering program."""
    # Load movie data from JSON file
    movies = load_movie_data()
    
    # Get filter criteria from the user
    genre, imdb_min, imdb_max, actor, start_year, end_year, age_certification = get_user_input()
    
    # Apply filters one by one based on the criteria specified
    movies = filter_by_genre(movies, genre)
    movies = filter_by_imdb_rating(movies, imdb_min, imdb_max)
    movies = filter_by_actor(movies, actor)
    movies = filter_by_year_range(movies, start_year, end_year)
    movies = filter_by_age_certification(movies, age_certification)
    
    # Display the filtered movies
    display_movies(movies)

# Run the program
if __name__ == "__main__":
    main()
