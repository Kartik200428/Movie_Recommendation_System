import pickle
import streamlit as st
import pandas as pd
import requests


# Function to fetch the movie poster from TMDB API
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=80f4c5c470a134e7f384776018b3a810'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        #debuging log
        #st.text(f"API Response for movie_id {movie_id}: {data}")

        # Check if 'poster_path' exists in the response
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            st.warning(f"No poster found for movie_id {movie_id}. Using fallback image.")
            return "https://via.placeholder.com/500"  # Fallback image
    except requests.exceptions.Timeout:
        st.error("Request timed out while fetching the poster. Try again later.")
        return "https://via.placeholder.com/500"
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the poster: {e}")
        return "https://via.placeholder.com/500"


# Function to recommend movies based on the selected movie
def recommend(movie):
    if movie not in movies['title'].values:
        st.error("Selected movie not found in the database.")
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        st.text(f"Fetching poster for movie_id: {movie_id}")  # Debugging log
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Load the data
movies_dict = pickle.load(open('.venv/mov_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('.venv/simi.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommendation System')
selected_movie_name = st.selectbox(
    'Which movie do you want to recommend?', movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    if names and posters:
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

# Debugging/Test API functionality
if st.button("Test API"):
    test_movie_id = 550  # Example movie ID (Fight Club)
    st.text(f"Testing API with movie_id: {test_movie_id}")
    poster_url = fetch_poster(test_movie_id)
    st.image(poster_url)
