import pandas as pd
import requests
import sqlite3
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
print(movies.head())
print(ratings.head())
movies["year"]= movies["title"].str.extract(r"\((\d{4})\)")
movies["title"] = movies["title"].str.replace(r"\(\d{4}\)", "", regex=True)
conn = sqlite3.connect("movies.db")
cursor= conn.cursor() 
with open("schema.sql") as f:
    conn.executescript(f.read())
for _, row in movies.iterrows():
 cursor.execute(""" INSERT OR IGNORE INTO MOVIES VALUES(?,?,?,?,?,?,?)""",
                   (
                       row["movieId"],
                       row["title"],
                       row["year"],
                       row["genres"],
                       None,
                       None,
                       None
                    ) )
ratings.to_sql("ratings", conn, if_exists="replace", index=False)
conn.commit()
conn.close()
print(movies.head())
def get_movies_details(title):
    url =f"http://www.omdbapi.com/?t={title}&apikey=44fb6217"
    response = requests.get(url)
    data = response.json()
    if data["Response"] == "True":
        return data["Director"],data["Plot"],data["BoxOffice"]
    return None,None,None
