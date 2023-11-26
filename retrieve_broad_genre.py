import json

def load_genre_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_lookup_table(data):
    lookup_table = {}
    for broad_genre, subgenres in data.items():
        for subgenre in subgenres:
            lookup_table[subgenre.lower()] = broad_genre
    return lookup_table

def get_broad_genre(subgenre, lookup_table):
    return lookup_table.get(subgenre, "Unknown Genre")

file_path = 'sorted_genres_for_search.json'
genre_data = load_genre_data(file_path)
genre_lookup_table = create_lookup_table(genre_data)

#Test code: uncomment to test
#input_subgenre = "Abstract Beats"
#broad_genre = get_broad_genre(input_subgenre, genre_lookup_table)
#print(f"The broad genre for '{input_subgenre}' is '{broad_genre}'.")
