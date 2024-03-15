
DROP DATABASE IF EXISTS blogly;
CREATE DATABASE blogly;

\c blogly


CREATE TABLE users
(
    id BIGSERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    image_url TEXT

);


CREATE TABLE posts
(
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT (CURRENT_DATE),
    user_id INTEGER NOT NULL REFERENCES users(id)

);


CREATE TABLE tags
(
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE post_tags
(
    id BIGSERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id),
    tag_id INTEGER NOT NULL REFERENCES tags(id)

);