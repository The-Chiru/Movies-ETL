TRUNCATE TABLE movie_genres, ratings, genres, movies RESTART IDENTITY CASCADE;

CREATE TABLE movies (
    movie_id INT PRIMARY KEY,
    title TEXT,
    release_year INT,
    director TEXT,
    plot TEXT,
    imdb_id TEXT,
    box_office TEXT
);

CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE movie_genres (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY(movie_id, genre_id),
    FOREIGN KEY(movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY(genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE ratings (
    user_id INT,
    movie_id INT,
    rating FLOAT,
    timestamp BIGINT,
    PRIMARY KEY(user_id, movie_id),
    FOREIGN KEY(movie_id) REFERENCES movies(movie_id)
);