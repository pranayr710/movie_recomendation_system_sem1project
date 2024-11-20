import pandas as pd
import json
def file():
    # Load the CSV file
    csv_file_path = r"C:\Users\91756\Desktop\all.csv"  # Path to the CSV file
    movie_data = pd.read_csv(csv_file_path)

    # Convert the CSV data to JSON format (records will return a list of dictionaries)
    movie_json = movie_data.to_dict(orient='records')

    # Write JSON data to a file
    json_file_path = 'movies_data.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(movie_json, json_file, indent=4)

    print(f"Data has been successfully converted to JSON and saved to {json_file_path}")

file()