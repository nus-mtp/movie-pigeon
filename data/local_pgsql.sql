CREATE TABLE bookmarks
(
    user_id INTEGER NOT NULL,
    imdb_id VARCHAR(32) NOT NULL,
    CONSTRAINT bookmarks_user_id_imdb_id_pk PRIMARY KEY (user_id, imdb_id),
    CONSTRAINT bookmarks_users_user_id_fk FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT bookmarks_movies_imdb_id_fk FOREIGN KEY (imdb_id) REFERENCES movies (imdb_id)
);
CREATE TABLE cinemas
(
    cinema_id INTEGER PRIMARY KEY NOT NULL,
    cinema_name VARCHAR(128) NOT NULL
);
CREATE UNIQUE INDEX cinemas_cinema_name_uindex ON cinemas (cinema_name);
CREATE TABLE general_recommend
(
    user_id INTEGER NOT NULL,
    imdb_id VARCHAR(32) NOT NULL,
    CONSTRAINT general_recommend_user_id_imdb_id_pk PRIMARY KEY (user_id, imdb_id),
    CONSTRAINT general_recommend_users_user_id_fk FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT general_recommend_movies_imdb_id_fk FOREIGN KEY (imdb_id) REFERENCES movies (imdb_id)
);
CREATE TABLE movies
(
    imdb_id VARCHAR(32) PRIMARY KEY NOT NULL,
    title VARCHAR(256) NOT NULL,
    production_year INTEGER DEFAULT 0,
    rated VARCHAR(32) DEFAULT 'unknown'::character varying NOT NULL,
    plot TEXT NOT NULL,
    language VARCHAR(32) NOT NULL,
    country VARCHAR(32) NOT NULL,
    poster_url TEXT NOT NULL
);
CREATE TABLE public_rating
(
    imdb_id VARCHAR(32) NOT NULL,
    source_id INTEGER NOT NULL,
    votes INTEGER DEFAULT 0,
    CONSTRAINT public_rating_imdb_id_source_id_pk PRIMARY KEY (imdb_id, source_id),
    CONSTRAINT public_rating_movies_imdb_id_fk FOREIGN KEY (imdb_id) REFERENCES movies (imdb_id),
    CONSTRAINT public_rating_rating_sources_source_id_fk FOREIGN KEY (source_id) REFERENCES rating_sources (source_id)
);
CREATE TABLE rating_sources
(
    source_id INTEGER PRIMARY KEY NOT NULL,
    source_name VARCHAR(32) NOT NULL
);
CREATE UNIQUE INDEX rating_sources_source_name_uindex ON rating_sources (source_name);
CREATE TABLE scales
(
    source_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    weight INTEGER,
    CONSTRAINT scales_source_id_user_id_pk PRIMARY KEY (source_id, user_id),
    CONSTRAINT scales_rating_sources_source_id_fk FOREIGN KEY (source_id) REFERENCES rating_sources (source_id),
    CONSTRAINT scales_users_user_id_fk FOREIGN KEY (user_id) REFERENCES users (user_id)
);
CREATE TABLE showing
(
    cinema_id INTEGER NOT NULL,
    imdb_id VARCHAR(32) NOT NULL,
    CONSTRAINT showing_cinema_id_imdb_id_pk PRIMARY KEY (cinema_id, imdb_id),
    CONSTRAINT showing_cinemas_cinema_id_fk FOREIGN KEY (cinema_id) REFERENCES cinemas (cinema_id),
    CONSTRAINT showing_movies_imdb_id_fk FOREIGN KEY (imdb_id) REFERENCES movies (imdb_id)
);
CREATE TABLE showing_recommend
(
    user_id INTEGER NOT NULL,
    imdb_id VARCHAR(32) NOT NULL,
    cinema_id INTEGER NOT NULL,
    CONSTRAINT showing_recommend_imdb_id_cinema_id_pk PRIMARY KEY (imdb_id, cinema_id),
    CONSTRAINT showing_recommend_users_user_id_fk FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT showing_recommend_movies_imdb_id_fk FOREIGN KEY (imdb_id) REFERENCES movies (imdb_id),
    CONSTRAINT showing_recommend_cinemas_cinema_id_fk FOREIGN KEY (cinema_id) REFERENCES cinemas (cinema_id)
);
CREATE TABLE user_rating
(
    user_id INTEGER NOT NULL,
    imdb_id VARCHAR(32) NOT NULL,
    rating INTEGER,
    CONSTRAINT user_rating_user_id_imdb_id_pk PRIMARY KEY (user_id, imdb_id),
    CONSTRAINT user_rating_users_user_id_fk FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT user_rating_movies_imdb_id_fk FOREIGN KEY (imdb_id) REFERENCES movies (imdb_id)
);
CREATE TABLE users
(
    user_id INTEGER PRIMARY KEY NOT NULL,
    email VARCHAR(256) NOT NULL,
    hashed_pass VARCHAR(128) NOT NULL
);
CREATE UNIQUE INDEX users_email_uindex ON users (email);

-- HARDCODED DATA --
-- websites sources name --
INSERT INTO rating_sources (source_name) VALUES ('IMDb');
INSERT INTO rating_sources (source_name) VALUES ('Metacritics');