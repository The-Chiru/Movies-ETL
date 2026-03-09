-- 1 Highest average rating movie

SELECT m.title, AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON m.movie_id = r.movie_id
GROUP BY m.title
ORDER BY avg_rating DESC
LIMIT 1;


-- 2 Top 5 genres by average rating

SELECT g.name, AVG(r.rating) AS avg_rating
FROM genres g
JOIN movie_genres mg ON g.genre_id = mg.genre_id
JOIN ratings r ON mg.movie_id = r.movie_id
GROUP BY g.name
ORDER BY avg_rating DESC
LIMIT 5;


-- 3 Director with most movies

SELECT director, COUNT(*) AS movie_count
FROM movies
WHERE director IS NOT NULL
GROUP BY director
ORDER BY movie_count DESC
LIMIT 1;


-- 4 Average rating per year

SELECT m.release_year, AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON m.movie_id = r.movie_id
GROUP BY m.release_year
ORDER BY m.release_year;