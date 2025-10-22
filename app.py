import streamlit as st
import  pickle
import pandas as pd
import requests
import os
import gdown
# https://drive.google.com/file/d/18Jdj-bmjy_hB24Wm07E8dKistrvi5aNn/view?usp=sharing
# https://drive.google.com/drive/folders/1PT3WslF6sH1XYj8KHXJjIl5WQ62nB1kb?usp=sharing
def download_from_drive(file_id, output_name):
    """Downloads a file from Google Drive if not already present"""
    if not os.path.exists(output_name):
        st.write("📥 Downloading large model file from Google Drive...")
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output_name, quiet=False)
        st.success("✅ Download complete.")
    else:
        st.write("✅ Model file already available locally.")

# Replace this with your real file ID from Drive
FILE_ID = "18Jdj-bmjy_hB24Wm07E8dKistrvi5aNn"
download_from_drive(FILE_ID, "similarity.pkl")



def fetch_poster(movie_id):
    try:
        omdb_api_key = "5a24876a"
        movie_title = movies.iloc[movies[movies['movie_id'] == movie_id].index[0]].title
        search_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie_title}&type=movie"
        response = requests.get(search_url)

        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=Error+Loading+Image"

        data = response.json()

        if data.get('Response') == 'True' and data.get('Poster') and data['Poster'] != 'N/A':
            return data['Poster']
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Found"
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Error+Loading+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = list(enumerate(distances))
    reco = []
    for i, j in movie_list:
        if i < len(movies):
            director_similarity = 0.3 * (int(movies['director'].iloc[i] == movies['director'].iloc[movie_index]))
            writer_similarity = 0.3 * (int(movies['writer'].iloc[i] == movies['writer'].iloc[movie_index]))
            total = j + director_similarity + writer_similarity
            reco.append(total)
    mo_list = sorted(list(enumerate(reco)), reverse=True, key=lambda x: x[1])[0:10]
    recommended_movies = []
    recommended_movies_posters = []
    for i in mo_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
select_movie_name = st.selectbox('Select a movie you like', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(select_movie_name)
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
        
    col6, col7, col8, col9, col10 = st.columns(5)
    with col6:
        st.text(names[5])
        st.image(posters[5])
    with col7:
        st.text(names[6])
        st.image(posters[6])
    with col8:
        st.text(names[7])
        st.image(posters[7])
    with col9:
        st.text(names[8])
        st.image(posters[8])
    with col10:
        st.text(names[9])
        st.image(posters[9])







