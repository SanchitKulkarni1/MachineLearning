# import pandas as pd

# class MovieRecommender:
#     def __init__(self, data_path, similarity_matrix):
#         # Load the merged movie data
#         self.movies = pd.read_csv(data_path)
#         self.similarity = similarity_matrix

#     def recommend(self, query):
#         results = {"type": "", "query": query, "recommendations": []}

#         # Check if the query matches a movie title
#         if query in self.movies['title'].values:
#             results["type"] = "title"
#             movie_index = self.movies[self.movies['title'] == query].index[0]
#             distances = self.similarity[movie_index]
#             movies_list = sorted(
#                 list(enumerate(distances)), reverse=True, key=lambda x: x[1]
#             )[1:6]
#             results["recommendations"] = [
#                 self.movies.iloc[i[0]]['title'] for i in movies_list
#             ]
#         else:
#             # Query is not a movie title: assume it's a tag
#             results["type"] = "tag"
#             tag_filtered_movies = self.movies[
#                 self.movies['tags'].str.contains(query, case=False, na=False)
#             ]

#             if tag_filtered_movies.empty:
#                 results["recommendations"] = []
#             else:
#                 results["recommendations"] = tag_filtered_movies['title'].head(5).tolist()

#         return results


import os
import openai
import pandas as pd
import numpy as np

class MovieRecommender:
    def __init__(self, data_path, similarity_matrix):
        # Load the movie data
        self.movies = pd.read_csv(data_path)
        self.similarity = similarity_matrix
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Load OpenAI API key

    def recommend(self, query):
        """
        Generate movie recommendations based on the query.
        """
        results = {"type": "", "query": query, "recommendations": []}

        # Check if the query matches a movie title
        if query in self.movies['title'].values:
            results["type"] = "title"
            movie_index = self.movies[self.movies['title'] == query].index[0]
            distances = self.similarity[movie_index]
            movies_list = sorted(
                list(enumerate(distances)), reverse=True, key=lambda x: x[1]
            )[1:6]
            results["recommendations"] = [
                self.movies.iloc[i[0]]['title'] for i in movies_list
            ]
        else:
            # Query is not a movie title: assume it's a tag
            results["type"] = "tag"
            tag_filtered_movies = self.movies[
                self.movies['tags'].str.contains(query, case=False, na=False)
            ]

            if tag_filtered_movies.empty:
                results["recommendations"] = []
            else:
                results["recommendations"] = tag_filtered_movies['title'].head(5).tolist()

        return results

    def chat(self, user_input):
        """
        Process user input and return a chatbot response.
        """
        # Try to provide recommendations based on the input
        recommendations = self.recommend(user_input)
        if recommendations["recommendations"]:
            # If recommendations are available, return them
            return f"Based on your query, here are some recommendations: {', '.join(recommendations['recommendations'])}."
        else:
            # Use OpenAI API for natural language response if no recommendations found
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful movie recommendation assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response['choices'][0]['message']['content']
            return reply


# Main function to run the chatbot
def main():
    # Load your movie data and similarity matrix
    data_path = "movies.csv"
    similarity_matrix = np.load("similarity_matrix.npy")  # Precomputed similarity matrix
    
    # Initialize the recommender
    recommender = MovieRecommender(data_path, similarity_matrix)
    
    # Chat loop
    print("Welcome to the Movie Recommender Chatbot! Type 'exit' to quit.")
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        response = recommender.chat(user_query)
        print(f"Bot: {response}")

# Run the chatbot
if __name__ == "__main__":
    main()
