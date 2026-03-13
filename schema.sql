CREATE TABLE IF NOT EXISTS movies(
    movie_id INTEGER PRIMARY KEY,
    titel TEXT,
    year INTEGER,
    geners TEXT,
    director TEXT,
    plot text,
    box_office TEXT
);
CREATE TABLE IF NOT EXISTS ratings (
    user_id INTEGER,
    movie_id INTEGER,
    rating REAL,
    timestamp INTEGER
);
