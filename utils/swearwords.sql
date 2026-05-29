DROP TABLE IF EXISTS BelongsTo CASCADE;
DROP TABLE IF EXISTS Has CASCADE;
DROP TABLE IF EXISTS Speaks CASCADE;
DROP TABLE IF EXISTS Word CASCADE;
DROP TABLE IF EXISTS Category CASCADE;
DROP TABLE IF EXISTS Language CASCADE;
DROP TABLE IF EXISTS Country CASCADE;

CREATE TABLE IF NOT EXISTS Country (
    country_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Language (
    language_code VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Category (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Word (
    word_id INT PRIMARY KEY,
    word VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Speaks (
    country_id INT REFERENCES Country(country_id) ON DELETE CASCADE,
    language_code VARCHAR(20) REFERENCES Language(language_code) ON DELETE CASCADE,
    PRIMARY KEY (country_id, language_code)
);

CREATE TABLE IF NOT EXISTS Has (
    language_code VARCHAR(20) REFERENCES Language(language_code) ON DELETE CASCADE,
    word_id INT REFERENCES Word(word_id) ON DELETE CASCADE,
    PRIMARY KEY (language_code, word_id)
);

CREATE TABLE IF NOT EXISTS BelongsTo (
    word_id INT REFERENCES Word(word_id) ON DELETE CASCADE,
    category_id INT REFERENCES Category(category_id) ON DELETE CASCADE,
    PRIMARY KEY (word_id, category_id)
);
