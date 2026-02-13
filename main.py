import streamlit as st
import pickle
import traceback
import os
import pandas as pd
import requests

# 🎬 Fetch movie poster from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a00191e5582273b2bcd0e737ba1a1421&language=en-US"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# ⭐ Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]

    movie_list = sorted(list(enumerate(distance)),
                        reverse=True,
                        key=lambda x: x[1])[1:6]

    recommended = []
    recommended_movies_poster = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended, recommended_movies_poster


st.write("App Started")

# Load pickle files
model_path = os.path.join(os.path.dirname(__file__), "movies.pkl")
model2 = os.path.join(os.path.dirname(__file__), "similarity.pkl")

try:
    movies = pickle.load(open(model_path, "rb"))
    similarity = pickle.load(open(model2, "rb"))
    st.success("MODEL LOADED SUCCESSFULLY")
except Exception as e:
    st.error("MODEL NOT LOADED SUCCESSFULLY")
    st.text(traceback.format_exc())
    st.stop()

# Convert to DataFrame
movies = pd.DataFrame(movies)

st.title('🎬 Movie Recommendation System')

selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)

# 🎯 Recommend button
if st.button("Recommend Movie"):
    names, posters = recommend(selected_movie_name)

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





