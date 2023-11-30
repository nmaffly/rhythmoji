import pandas as pd 
import os
import random

current_directory = os.getcwd()
file_path = os.path.join(current_directory, 'genre_to_clothing.csv')
genre_to_clothing_df = pd.read_csv(file_path)

assigned_clothing = [('Shirts', 'Hip-Hop/Rap'), ('Pants', 'Rock'), ('Headwear', 'Pop'), ('Accessories', 'Alternative'), ('Shoes', 'Hip-Hop/Rap')]

for i, (clothes, genre) in enumerate(assigned_clothing):
    result = genre_to_clothing_df[genre_to_clothing_df['Genres'] == genre][clothes].values
    if len(result) > 0:
        result_list = result[0].split(', ')
        random_clothing = random.choice(result_list)
        print(random_clothing)
        assigned_clothing[i] = (clothes, random_clothing)


print(assigned_clothing)