CREATE TABLE IF NOT EXISTS password_table (
    username TEXT NOT NULL,
    website_username TEXT NOT NULL,
    website TEXT NOT NULL,
    password TEXT,
    PRIMARY KEY (username, website)
);


CREATE TABLE IF NOT EXISTS login_table (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
