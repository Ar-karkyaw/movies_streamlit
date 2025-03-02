import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the pre-merged data
movies = pd.read_csv("processed_movies.csv")

# Streamlit app title
st.title("映画データダッシュボード")

# Display data overview
st.header("映画データの概要")
st.write(movies.head())

# 評価分布
st.header("平均評価の分布")
fig, ax = plt.subplots()
sns.histplot(movies['averageRating'], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# 年によるフィルタ
st.sidebar.header("フィルター")
year_range = st.sidebar.slider("年範囲を選択", int(movies["startYear"].min()), int(movies["startYear"].max()), (2000, 2020))
filtered_movies = movies[(movies['startYear'] >= year_range[0]) & (movies['startYear'] <= year_range[1])]

# フィルタリングされたデータを表示
st.subheader(f"{year_range[0]}年から{year_range[1]}年までに公開された映画")
st.write(filtered_movies[['primaryTitle', 'startYear', 'averageRating', 'numVotes']])


# Rating vs. Number of Votes Scatter Plot
st.header("評価と投票数の散布図")
min_votes, max_votes = st.sidebar.slider(
    "投票数でフィルター",
    int(movies["numVotes"].min()), int(movies["numVotes"].max()), (1000, 100000)
)
filtered_votes = movies[(movies["numVotes"] >= min_votes) & (movies["numVotes"] <= max_votes)]
fig, ax = plt.subplots()
ax.scatter(filtered_votes["numVotes"], filtered_votes["averageRating"], alpha=0.5)
ax.set_xlabel("Number of Votes")
ax.set_ylabel("Average Rating")
st.pyplot(fig)

# Top Movies by Genre
selected_genre = st.sidebar.selectbox("ジャンルを選択", movies["genres"].str.split(',').explode().unique())
genre_movies = movies[movies["genres"].str.contains(selected_genre, na=False)]
st.header(f"ジャンル別トップ10映画 ({selected_genre})")
top_genre_movies = genre_movies.sort_values(by="averageRating", ascending=False).head(10)
st.write(top_genre_movies[["primaryTitle", "startYear", "averageRating", "numVotes"]])

# Interactive Filters for Ratings and Genres
st.header("評価とジャンルで映画をフィルタリング")
min_rating, max_rating = st.sidebar.slider(
    "平均評価でフィルター",
    float(movies["averageRating"].min()), float(movies["averageRating"].max()), (6.0, 9.0)
)
filtered_movies = movies[(movies["averageRating"] >= min_rating) & (movies["averageRating"] <= max_rating)]
genres = st.sidebar.multiselect(
    "ジャンルを選択",
    options=movies["genres"].str.split(',').explode().unique(),
    default=["Action"]
)
filtered_movies = filtered_movies[filtered_movies["genres"].apply(lambda x: all(genre in x for genre in genres))]
st.write(filtered_movies.head())


st.header("投票数の多いトップ映画")
top_voted_movies = movies.sort_values(by="numVotes", ascending=False).head(10)
st.write(top_voted_movies[["primaryTitle", "startYear", "averageRating", "numVotes"]])

st.header("ジャンルの頻度分析")
from collections import Counter
genres_list = movies['genres'].str.split(',').explode().tolist()
genre_counts = pd.DataFrame(Counter(genres_list).items(), columns=["genre", "count"]).sort_values(by="count", ascending=False)
fig, ax = plt.subplots()
sns.barplot(x="count", y="genre", data=genre_counts, ax=ax)
ax.set_xlabel("Number of Movies")
ax.set_ylabel("Genre")
st.pyplot(fig)

