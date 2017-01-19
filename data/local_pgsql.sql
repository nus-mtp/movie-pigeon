CREATE TABLE movies
(
    imdb_id VARCHAR(32) PRIMARY KEY NOT NULL,
    title VARCHAR(128) NOT NULL,
    production_year INTEGER,
    rated VARCHAR(16),
    release_time DATE NOT NULL,
    length INTEGER NOT NULL,
    genre VARCHAR(128) NOT NULL,
    director VARCHAR(128) NOT NULL,
    column_10 INTEGER,
    actors TEXT NOT NULL,
    plot TEXT,
    language VARCHAR(128),
    country VARCHAR(128) NOT NULL,
    poster_url TEXT NOT NULL
);
CREATE UNIQUE INDEX movies_imdb_id_uindex ON movies (imdb_id);

CREATE TABLE ratings
(
    imdb_id VARCHAR(32) PRIMARY KEY NOT NULL,
    metacritic INTEGER NOT NULL,
    imdb INTEGER,
    rottentomatoes INTEGER,
    letterboxd INTEGER,
    fandango INTEGER,
    douban INTEGER,
    CONSTRAINT ratings_movies_imdb_id_fk FOREIGN KEY (imdb_id) REFERENCES movies (imdb_id)
);

CREATE TABLE votes
(
    imdb_id VARCHAR(32) PRIMARY KEY NOT NULL,
    metacritic INTEGER NOT NULL,
    imdb INTEGER,
    rottentomatoes INTEGER,
    letterboxd INTEGER,
    fandango INTEGER,
    douban INTEGER,
    CONSTRAINT ratings_movies_imdb_id_fk FOREIGN KEY (imdb_id) REFERENCES movies (imdb_id)
);