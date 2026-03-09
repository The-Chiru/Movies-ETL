import pandas as pd
import requests
from sqlalchemy import create_engine, text

# ---------------------------
# CONFIG
# ---------------------------

OMDB_API_KEY = "7f6fa8a0"

MOVIES_FILE = "data/movies.csv"
RATINGS_FILE = "data/ratings.csv"

DB_URL = "postgresql://movieuser:moviepass@localhost:5432/moviesdb"

engine = create_engine(DB_URL)


# ---------------------------
# LOAD CSV FILES
# ---------------------------

print("Loading CSV files...")

movies_df = pd.read_csv(MOVIES_FILE)
ratings_df = pd.read_csv(RATINGS_FILE)


# ---------------------------
# TRANSFORM MOVIES DATA
# ---------------------------

print("Transforming movies data...")

movies_df["release_year"] = movies_df["title"].str.extract(r"\((\d{4})\)")
movies_df["title"] = movies_df["title"].str.replace(r"\(\d{4}\)", "", regex=True).str.strip()

movies_df = movies_df.rename(columns={"movieId": "movie_id"})

movies_df["release_year"] = pd.to_numeric(movies_df["release_year"], errors="coerce")


# ---------------------------
# OMDB API FUNCTION
# ---------------------------

def fetch_movie_details(title):

    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"

    try:
        response = requests.get(url).json()

        if response["Response"] == "True":

            return {
                "director": response.get("Director"),
                "plot": response.get("Plot"),
                "imdb_id": response.get("imdbID"),
                "box_office": response.get("BoxOffice")
            }

    except:
        pass

    return {
        "director": None,
        "plot": None,
        "imdb_id": None,
        "box_office": None
    }


# ---------------------------
# FETCH API DATA
# ---------------------------

print("Fetching OMDb data...")

movies_df = movies_df.head(100)   # limit API calls

directors = []
plots = []
imdb_ids = []
box_offices = []

for title in movies_df["title"]:

    data = fetch_movie_details(title)

    directors.append(data["director"])
    plots.append(data["plot"])
    imdb_ids.append(data["imdb_id"])
    box_offices.append(data["box_office"])


movies_df["director"] = directors
movies_df["plot"] = plots
movies_df["imdb_id"] = imdb_ids
movies_df["box_office"] = box_offices


# ---------------------------
# LOAD MOVIES
# ---------------------------

print("Loading movies table...")

movies_df[[
    "movie_id",
    "title",
    "release_year",
    "director",
    "plot",
    "imdb_id",
    "box_office"
]].to_sql("movies", engine, if_exists="replace", index=False)


# ---------------------------
# LOAD RATINGS
# ---------------------------

print("Loading ratings table...")

ratings_df = ratings_df.rename(columns={"userId": "user_id", "movieId": "movie_id"})

# keep only ratings for movies we loaded
ratings_df = ratings_df[ratings_df["movie_id"].isin(movies_df["movie_id"])]

ratings_df.to_sql("ratings", engine, if_exists="append", index=False)

# ---------------------------
# GENRE NORMALIZATION
# ---------------------------

print("Processing genres...")

from sqlalchemy import text

conn = engine.connect()

for _, row in movies_df.iterrows():

    movie_id = row["movie_id"]
    genres = row["genres"].split("|")

    for genre in genres:

        conn.execute(
            text("INSERT INTO genres(name) VALUES(:genre) ON CONFLICT DO NOTHING"),
            {"genre": genre}
        )

        result = conn.execute(
            text("SELECT genre_id FROM genres WHERE name=:genre"),
            {"genre": genre}
        ).fetchone()

        genre_id = result[0]

        conn.execute(
            text("""
                INSERT INTO movie_genres(movie_id, genre_id)
                VALUES(:movie_id, :genre_id)
                ON CONFLICT DO NOTHING
            """),
            {"movie_id": movie_id, "genre_id": genre_id}
        )

conn.commit()

print("ETL Pipeline Completed ✅")