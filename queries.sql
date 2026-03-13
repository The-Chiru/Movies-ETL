-- Question 1: Highest average rating movie
SELECT m.titel, AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r
ON m.movie_id = r.movieID
GROUP BY m.titel
ORDER BY avg_rating DESC
LIMIT 1;


-- Question 2: Top 5 genres
SELECT m.geners, AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r
ON m.movie_id = r.movieID
GROUP BY m.geners
ORDER BY avg_rating DESC
LIMIT 5;


--Director with most movies
SELECT Director, COUNT(*) AS movie_count
FROM movies
GROUP BY director
ORDER BY movie_count DESC
LIMIT 1;

--Average rating per year
SELECT YEAR ,AVG(r.rating)
FROM movies m
JOIN ratings r
ON m.movie_id = r.movieID
GROUP BY YEAR
ORDER BY YEAR;
