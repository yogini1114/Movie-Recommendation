import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

def download_from_drive(file_id, output):
    url = f"https://drive.google.com/uc?id={file_id}"
    if not os.path.exists(output):
        print(f"Downloading {output}...")
        gdown.download(url, output, quiet=False)

# 🔹 Replace these IDs with your actual ones
movie_dict_id = "13ISaA8p6gl90P2mSbUby6UAtRFNKiY5d"
similarity_id = "1_RcwC5YySGtNAHwo-9EZmbwXO37R-hTm"

# File names
movie_dict_file = "movie_dict.pkl"
similarity_file = "similarity.pkl"

# Download both
download_from_drive(movie_dict_id, movie_dict_file)
download_from_drive(similarity_id, similarity_file)

# Load both
movies_dict = pickle.load(open(movie_dict_file, "rb"))
similarity = pickle.load(open(similarity_file, "rb"))

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise RuntimeError("TMDB_API_KEY not set in environment")

def fetch_poster(movie_id):

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=fa28d331c77722cbee5fad253b59dda8"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            # Use properly URL encoded placeholder text
            return "https://via.placeholder.com/300x450?text=No%20Image%20Available"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/300x450?text=No%20Image%20Available"



def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommend_movies_posters = []
    for i in movies_list:  # skip the first one (the movie itself)
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommend_movies_posters

movies_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')
selected_movie_name= st.selectbox(
'ENTER A MOVIE',
movies['title'].values)

if st.button('RECOMMEND'):
    names,posters=recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])



