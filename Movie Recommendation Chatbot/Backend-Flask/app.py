from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
from recommender import MovieRecommender

app = Flask(__name__)
CORS(app)

# Load preprocessed merged data and similarity matrix
data_path = "data/merged_movies.csv"
similarity_matrix_path = "data/similarity.pkl"

with open(similarity_matrix_path, "rb") as file:
    similarity_matrix = pickle.load(file)

# Initialize the recommender
recommender = MovieRecommender(data_path, similarity_matrix)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Get recommendations
    recommendations = recommender.recommend(query)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
