CREATE VIRTUAL TABLE gifpolis USING fts4 (
    uuid TEXT,
    description TEXT NOT NULL,
    file TEXT NOT NULL,
    PRIMARY KEY (uuid)
);