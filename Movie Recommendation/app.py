# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import ast

# Step 1: Load the dataset
df = pd.read_csv('moviedata.csv')

# Step 2: Data Preprocessing
# Keep relevant columns
df = df[['title', 'genres', 'overview', 'keywords', 'vote_average', 'vote_count']]

# Drop rows with missing values in critical columns
df = df.dropna(subset=['title', 'genres', 'overview', 'keywords'])

# Function to convert JSON-like strings into lists of genres/keywords
def convert_to_list(data):
    if pd.isna(data):
        return []
    else:
        return [d['name'] for d in ast.literal_eval(data)]

# Apply conversion to genres and keywords columns
df['genres'] = df['genres'].apply(convert_to_list)
df['keywords'] = df['keywords'].apply(convert_to_list)

# Combine genres, keywords, and overview into a single 'features' column
df['features'] = df['genres'].astype(str) + ' ' + df['keywords'].astype(str) + ' ' + df['overview']

# Step 3: Feature Extraction using TF-IDF
# Use TF-IDF Vectorizer to vectorize the 'features' column
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['features'])

# Step 4: Compute the Cosine Similarity Matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Step 5: Create a Function to Recommend Movies
# Create a mapping from movie title to index
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

# Function to get movie recommendations based on cosine similarity
def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    if title not in indices.index:
        return []
    idx = indices[title]
    
    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the indices of the 10 most similar movies
    sim_scores = sim_scores[1:11]
    
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    
    # Return the top 10 most similar movies
    return df['title'].iloc[movie_indices]

# Step 6: Build the Streamlit App
# Streamlit app title
st.title('Movie Recommendation System')

# User input for movie title
movie = st.text_input('Enter a movie title:')

# Button to get recommendations
if st.button('Get Recommendations'):
    recommendations = get_recommendations(movie)
    if len(recommendations) > 0:
        st.write(f"Movies similar to {movie}:")
        for rec in recommendations:
            st.write(rec)
    else:
        st.write('Movie not found in dataset.')

