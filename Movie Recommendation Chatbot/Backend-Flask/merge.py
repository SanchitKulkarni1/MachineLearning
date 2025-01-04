import pandas as pd

# Load datasets
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")
print("Movies columns:", movies.columns)
print("Credits columns:", credits.columns)

# Merge datasets on a common column (e.g., 'id')
movies = movies.merge(credits, on="title")

# Create a 'tags' column for recommendations
def preprocess(row):
    return f"{row['genres']} {row['overview']} {row['cast']} {row['crew']}"

movies['tags'] = movies.apply(preprocess, axis=1)

# Save the combined dataset for later use
movies.to_csv("data/merged_movies.csv", index=False)
