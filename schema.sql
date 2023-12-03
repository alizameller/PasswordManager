CREATE TABLE IF NOT EXISTS password_table (
    username TEXT NOT NULL,
    website TEXT NOT NULL,
    password TEXT,
    PRIMARY KEY (username, website)
);

