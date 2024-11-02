import streamlit as st
import pandas as pd
import pickle
import requests
st.title("Recommendation System")
with open('titles.pkl', 'rb') as file:
    movies = pickle.load(file)
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)
titles = list(movies.keys())
movie_ids=list(movies.values())
movie = st.selectbox("Enter the name of the movie", tuple(titles))
def get_movie_poster(movie_id, api_key):
    base_url = "https://api.themoviedb.org/3/movie/"
    url = f"{base_url}{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return poster_url
        else:
            return "Poster not available."
    else:
        return f"Error: {response.status_code}"
def predict(movie,api_key):
    index = titles.index(movie)
    res = [i[0] for i in sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)][1:10]
    res2=[titles[i] for i in res]
    res3=[get_movie_poster(movie_ids[i],api_key) for i in res]
    return res2,res3
API_KEY=None
if st.button("Predict",type="primary"):
    pred,ids=predict(movie,API_KEY)
    col1, col2, col3, col4,col5 = st.columns(5)
    with col1:
        st.header(pred[0])
        st.image(ids[0])
    with col2:
        st.header(pred[1])
        st.image(ids[1])
    with col3:
        st.header(pred[2])
        st.image(ids[2])
    with col4:
        st.header(pred[3])
        st.image(ids[3])
    with col5:
        st.header(pred[4])
        st.image(ids[4])
