
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
