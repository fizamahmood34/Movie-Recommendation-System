# app.py
import streamlit as st
import pandas as pd
import requests
import pickle

# Load movie data
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Get Recommendations"):
    idx = movies[movies['title'] == selected_movie].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]

    recommended_titles = movies['title'].iloc[movie_indices].values
    recommended_ids = movies['movie_id'].iloc[movie_indices].values

    st.write("Top 10 Recommended Movies:")

    for i in range(0, 10, 5):
        cols = st.columns(5)
        for j, col in zip(range(i, i+5), cols):
            if j < len(recommended_titles):
                title = recommended_titles[j]
                movie_id = recommended_ids[j]
                poster_url = None
                try:
                    api_key = '9489612d3cf8eca592c1cb3f71976122'
                    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
                    response = requests.get(url)
                    data = response.json()
                    if data.get('poster_path'):
                        poster_url = "https://image.tmdb.org/t/p/w500" + data['poster_path']
                except:
                    pass

                with col:
                    if poster_url:
                        st.image(poster_url, width=150)
                    st.write(title)
