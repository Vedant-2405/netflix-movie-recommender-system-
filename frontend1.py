import streamlit as st
import pickle
import requests

st.set_page_config(page_title="Movie Recommendation System", layout="wide")
st.title("🎬 Movie Recommendation System")

API_KEY = "697d2f68cef90c409383faa30d043275"

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies['title'].values


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return None
    except:
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    sim_scores = similarity[movie_index]
    similar_indices = sim_scores.argsort()[::-1][1:6]

    names = []
    posters = []

    for idx in similar_indices:
        movie_id = movies.iloc[idx].movie_id
        names.append(movies.iloc[idx].title)
        posters.append(fetch_poster(movie_id))

    return names, posters

with st.form("recommendation_form"):
    selected_movie_name = st.selectbox(
        "Select a Movie:",
        movies_list,
        index=None,         
        placeholder="Select a movie"
    )
    submitted = st.form_submit_button("Recommend")

if submitted:
    names, posters = recommend(selected_movie_name)

    st.subheader("Recommended Movies")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            if posters[i]:
                st.image(posters[i])
            else:
                st.write("Poster not available")