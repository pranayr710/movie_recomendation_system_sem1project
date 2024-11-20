import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

# Load JSON data from the file
def load_movie_data(json_file_path='movies_data.json'):
    """Loads movie data from a JSON file."""
    with open(json_file_path, 'r') as file:
        movies = json.load(file)
    return movies

# AI-based movie recommendation (based on IMDb rating)
def recommend_best_movie(filtered_movies):
    """Recommends the best movie based on IMDb rating."""
    if filtered_movies:
        best_movie = max(filtered_movies, key=lambda x: x.get("Imdb", 0))
        return best_movie['Title'], best_movie['Imdb']
    return None, None

# Filter movies based on criteria
def filter_movies(movies, genre, imdb_min, imdb_max, actor, start_year, end_year, age_certification):
    """Filters movies based on multiple criteria, allowing 'none' or empty values to skip criteria."""
    # Normalize "none" entries to skip filtering for that field
    if genre.lower() == 'none' or genre == '':
        genre = None
    if imdb_min == 'none' or imdb_min == '':
        imdb_min = None
    else:
        imdb_min = float(imdb_min)
    if imdb_max == 'none' or imdb_max == '':
        imdb_max = None
    else:
        imdb_max = float(imdb_max)
    if actor.lower() == 'none' or actor == '':
        actor = None
    if start_year == 'none' or start_year == '':
        start_year = None
    else:
        start_year = int(start_year)
    if end_year == 'none' or end_year == '':
        end_year = None
    else:
        end_year = int(end_year)
    if age_certification.lower() == 'none' or age_certification == '':
        age_certification = None

    # Apply filtering based on available criteria
    if genre:
        movies = [movie for movie in movies if genre.lower() in movie.get("Genre", "").lower()]
    if imdb_min is not None:
        movies = [movie for movie in movies if movie.get("Imdb") >= imdb_min]
    if imdb_max is not None:
        movies = [movie for movie in movies if movie.get("Imdb") <= imdb_max]
    if actor:
        movies = [movie for movie in movies if actor.lower() in movie.get("Actor", "").lower()]
    if start_year and end_year:
        movies = [movie for movie in movies if start_year <= movie.get("Year") <= end_year]
    if age_certification:
        movies = [movie for movie in movies if movie.get("Age Certification") == age_certification.upper()]  # Fix: Ensure matching capitalization

    return movies
                                                                                                                   
# Display filtered movie data in the GUI                                                                                                                   
def display_movies(movies, listbox):                                                                               
    """Displays a list of filtered movies in the listbox."""                                                          # Display filtered movie after  checking all the conditions
    listbox.delete(0, tk.END)                                                                                         #this function(display movies) is to show the movies in the list box
    if movies:                                                                                                        # iterates through all the movies in the whole of the movies data set(which are filtered out after checking all the conditions)           
        for movie in movies:                                                                                          #Displays a list of filtered movies in the listbox(the pop up screen where list of filtered movies are displayed)
            listbox.insert(tk.END, f"Title: {movie['Title']}, Year: {movie['Year']}, IMDb: {movie['Imdb']}")          #(tk.end)cleares all the previous data  from the list box so that current movies wil be available to be printed there)                                                                                                                     
    else:                                                                                                             #inserts the text at the end of the listbox (appending each new entry below the previous one).
        listbox.insert(tk.END, "No movies match the specified criteria.")                         

# Update the recommendations based on filtered movies(mainly used to filter out that is to find the best movie among the filtered movies)
def show_recommendation(filtered_movies, recommendation_label):
#Shows the best movie recommendation based on IMDb rating.
    best_movie_title, best_movie_imdb = recommend_best_movie(filtered_movies)
    if best_movie_title:
        recommendation_label.config(text=f"Recommended Movie: {best_movie_title} (IMDb: {best_movie_imdb})")
    else:
        recommendation_label.config(text="No movie recommendation available.")

# Validate year input
def validate_year_input(start_year_entry, end_year_entry):
    """Validates if the start year is less than the end year and if the year is a valid integer."""
    try:                                                                                                    #(The try block starts here, allowing the program to attempt the validation process while handling any exceptions that might occur.)
        start_year = start_year_entry.get().lower()                                                         #(.get() is used to get the text content from each entry)
        end_year = end_year_entry.get().lower()
        if start_year != '' and end_year != '':                                                             #this line checks if  both start_year and end_year are not empty strings. If either one is empty it will assume that the input is not given and can be skipped
            start_year = int(start_year)
            end_year = int(end_year)                                                                                
            if start_year > end_year:
                messagebox.showerror("Invalid Year Range", "Start year cannot be greater than end year.")     #this shows the message based the given  data of st year and end yr
                return False
        return True
    except ValueError:
        messagebox.showerror("Invalid Year", "Please enter valid years.")
        return False

# Validate IMDb rating input  almost same as that of year block 
def validate_imdb_rating(imdb_min_combobox, imdb_max_combobox):
    """Validates if the IMDb rating is within range and if min rating is not higher than max rating."""
    imdb_min = imdb_min_combobox.get().lower()
    imdb_max = imdb_max_combobox.get().lower()
    try:
        if imdb_min != '' and imdb_max != '':
            imdb_min = float(imdb_min)
            imdb_max = float(imdb_max)
            if imdb_min > imdb_max:
                messagebox.showerror("Invalid IMDb Range", "Min IMDb cannot be higher than Max IMDb.")
                return False
        return True
    except ValueError:
        messagebox.showerror("Invalid IMDb Rating", "Please select valid IMDb ratings.")
        return False

# Function to get inputs from the user and filter movies
def on_filter_button_click(movies, genre_combobox, imdb_min_combobox, imdb_max_combobox, actor_entry,
start_year_entry, end_year_entry, certification_combobox, listbox, recommendation_label,
ai_recommendation_label):
    """Handles the filtering and displaying of movies based on user input."""
    genre = genre_combobox.get()                                                #(combobox in gui is used to provide a drop down)
    imdb_min = imdb_min_combobox.get()
    imdb_max = imdb_max_combobox.get()
    actor = actor_entry.get().lower()
    if not validate_imdb_rating(imdb_min_combobox, imdb_max_combobox):
        return
    if not validate_year_input(start_year_entry, end_year_entry):
        return
    start_year = start_year_entry.get().lower()
    end_year = end_year_entry.get().lower()
    age_certification = certification_combobox.get().lower()  # Capture the age certification

    # Filter movies based on input
    filtered_movies = filter_movies(movies, genre, imdb_min, imdb_max, actor, start_year, end_year, age_certification)

    # Display filtered movies
    display_movies(filtered_movies, listbox)

    # Show the best movie recommendation based on IMDb rating
    show_recommendation(filtered_movies, recommendation_label)

    # Show AI-based best movie recommendation
    best_ai_movie_title, best_ai_movie_imdb = recommend_best_movie(filtered_movies)
    if best_ai_movie_title:
        ai_recommendation_label.config(text=f"AI Best Recommendation: {best_ai_movie_title} (IMDb: {best_ai_movie_imdb})")                                         #.configuration is used for updation(here ai movie recomendation function)
    else:
        ai_recommendation_label.config(text="No AI recommendation available.")

# Function to reset all inputs
def reset_inputs(genre_combobox, imdb_min_combobox, imdb_max_combobox, actor_entry, start_year_entry,
end_year_entry, certification_combobox, listbox, recommendation_label, ai_recommendation_label):
    """Resets all input fields to their default values."""
    genre_combobox.set('')
    imdb_min_combobox.set('')
    imdb_max_combobox.set('')
    actor_entry.delete(0, tk.END)
    start_year_entry.delete(0, tk.END)
    end_year_entry.delete(0, tk.END)
    certification_combobox.set('')
    listbox.delete(0, tk.END)
    recommendation_label.config(text="Recommended Movie: None")
    ai_recommendation_label.config(text="AI Best Recommendation: None")

# Main function to create the GUI
def create_gui():
    """Creates and runs the movie filtering GUI."""
    # Load movie data
    movies = load_movie_data()

    # Create the main window
    window = tk.Tk()
    window.title("Movie Filter and Recommendation System")  #(window.title  sets the title of the main window.)
    window.geometry("1360x900")                             # to display the window on the screen 
    window.resizable(False, False)                          # window.resizable controls whether the window can be resized by the user in this first argument for width second for height

    # Add a welcome label
    welcome_label = tk.Label(window, text="Welcome to the Movie Recommendation System", font=("Arial", 18, "bold"))    #tk.Label() is a method from the tkinter library creates a label widget, which is a text display element 
    welcome_label.grid(row=0, column=0, columnspan=2, pady=20)            #pady=20 adds vertical padding (spacing) of 20 pixels above and below the label, creating space                                             # font=("Arial", 18, "bold") sets the font styling for the label text. "Arial" specifies the type of font,18 is the font size."bold" makes the text bold.
    
    # Filter criteria frame
    filter_frame = tk.LabelFrame(window, text="Filter Criteria", font=("Arial", 14), padx=15, pady=15)                                                 # padx(measurred inpixles)add horizontal padding (spacing) around a widget adds extra space on the left and right sides of a widget..
    filter_frame.grid(row=1, column=0, columnspan=2, padx=30, pady=20, sticky="ew")                                                                    # sticky="ew" option is used with the .grid() geometry manager sticky="ew", you're telling the widget to stick to both the left(e) and right(w) sides of its cell, making it expand horizontally to fill the entire width of the cell.

    # Genre Dropdown
    genre_label = tk.Label(filter_frame, text="Select Genre:", font=("Arial", 12))
    genre_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    genre_combobox = ttk.Combobox(filter_frame, values=["Horror", "Comedy", "Action", "Drama", "Romantic", "Thriller"], font=("Arial", 12))             # The ttk.Combobox is a widget in the tkinter library, which is a standard GUI toolkit in Python
    genre_combobox.grid(row=0, column=1, padx=10, pady=10)                                                                                              #pady is a parameter used to add vertical (top and bottom) padding around a widget. Padding is extra space added outside the widget's border, which helps position the widget with space around it, improving readability and visual layout in the GUI

    # IMDb Rating Dropdown
    imdb_min_label = tk.Label(filter_frame, text="Min IMDb Rating:", font=("Arial", 12))
    imdb_min_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    imdb_min_combobox = ttk.Combobox(filter_frame, values=[str(i) for i in range(0, 11)], font=("Arial", 12))
    imdb_min_combobox.grid(row=1, column=1, padx=10, pady=10)

    imdb_max_label = tk.Label(filter_frame, text="Max IMDb Rating:", font=("Arial", 12))
    imdb_max_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    imdb_max_combobox = ttk.Combobox(filter_frame, values=[str(i) for i in range(0, 11)], font=("Arial", 12))
    imdb_max_combobox.grid(row=2, column=1, padx=10, pady=10)

    # Actor Entry
    actor_label = tk.Label(filter_frame, text="Actor's Name:", font=("Arial", 12))
    actor_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    actor_entry = tk.Entry(filter_frame, font=("Arial", 12))
    actor_entry.grid(row=3, column=1, padx=10, pady=10)

    # Start Year Entry
    start_year_label = tk.Label(filter_frame, text="Start Year:", font=("Arial", 12))
    start_year_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
    start_year_entry = tk.Entry(filter_frame, font=("Arial", 12))
    start_year_entry.grid(row=4, column=1, padx=10, pady=10)

    # End Year Entry
    end_year_label = tk.Label(filter_frame, text="End Year:", font=("Arial", 12))
    end_year_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
    end_year_entry = tk.Entry(filter_frame, font=("Arial", 12))
    end_year_entry.grid(row=5, column=1, padx=10, pady=10)

    # Age Certification Dropdown
    certification_label = tk.Label(filter_frame, text="Age Certification:", font=("Arial", 12))
    certification_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")
    certification_combobox = ttk.Combobox(filter_frame, values=["U", "U/A", "A", "S"], font=("Arial", 12))
    certification_combobox.grid(row=6, column=1, padx=10, pady=10)

    # Filter Button
    filter_button = tk.Button(filter_frame, text="Filter Movies", font=("Arial", 12, "bold"),
    command=lambda: on_filter_button_click(movies, genre_combobox, imdb_min_combobox,
    imdb_max_combobox, actor_entry,
    start_year_entry, end_year_entry, certification_combobox,
    listbox, recommendation_label, ai_recommendation_label))
    filter_button.grid(row=2, column=15, pady=20)

    # Reset Button
    reset_button = tk.Button(filter_frame, text="Reset", font=("Arial", 12, "bold"),
     command=lambda: reset_inputs(genre_combobox, imdb_min_combobox, imdb_max_combobox, actor_entry,
    start_year_entry, end_year_entry, certification_combobox,
    listbox, recommendation_label, ai_recommendation_label))
    reset_button.grid(row=2, column=30, pady=20)

    # Movie Listbox to display filtered movies
    listbox = tk.Listbox(window, width=80, height=10, font=("Arial", 12))
    listbox.grid(row=2, column=0, columnspan=2, padx=30, pady=20)

    # Recommended Movie Label
    recommendation_label = tk.Label(window, text="Recommended Movie: None", font=("Arial", 14))
    recommendation_label.grid(row=3, column=0, columnspan=2, pady=20)

    # AI-based Movie Recommendation Label
    ai_recommendation_label = tk.Label(window, text="AI Best Recommendation: None", font=("Arial", 14))
    ai_recommendation_label.grid(row=4, column=0, columnspan=2, pady=20)

    # Run the application
    window.mainloop()


# Call the function to create the GUI
if __name__=="__main__":
    create_gui()
