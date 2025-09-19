import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np   # 🔴 CHANGE HERE: numpy import zaroori hai

# ---------------- FETCH POSTER FUNCTION ----------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=fa28d331c77722cbee5fad253b59dda8&language=en-US"
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# ---------------- LOAD FILES ----------------
# 🔴 CHANGE HERE: make sure movies.pkl and similarity.pkl correct banaye ho (jaise maine upar steps me bataya)
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
similarity = np.array(similarity)   # 🔴 CHANGE HERE: ensure numpy array

# Reset index to avoid mismatch
movies = pd.DataFrame(movies).reset_index(drop=True)

# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie):
    movie = movie.strip().lower()
    movies['title'] = movies['title'].str.strip().str.lower()

    if movie not in movies['title'].values:
        st.error(f"Movie '{movie}' not found in database.")
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]

    # 🔴 CHANGE HERE: convert distances to float
    distances = similarity[movie_index].astype(float)

    # sort with distance
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = int(movies.iloc[i[0]].movie_id)  # 🔴 CHANGE HERE: ensure movie_id column exists in movies.pkl
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ---------------- STREAMLIT UI ----------------
st.title("Movie Recommender System")

selected_movie_name = st.text_input("ENTER A MOVIE")

if st.button("RECOMMEND"):
    if selected_movie_name:
        names, posters = recommend(selected_movie_name)
        if names:
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.text(names[idx])
                    st.image(posters[idx])
