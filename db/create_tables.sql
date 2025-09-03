CREATE TABLE IF NOT EXISTS pvz (
    id UUID DEFAULT gen_random_uuid(),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    city VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS reception (
    id UUID DEFAULT gen_random_uuid(),
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pvz_id UUID,
    status VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (pvz_id) REFERENCES pvz (id)
);

CREATE TABLE IF NOT EXISTS product (
    id UUID DEFAULT gen_random_uuid(),
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type VARCHAR(255),
    reception_id UUID,
    PRIMARY KEY (id),
    FOREIGN KEY (reception_id) REFERENCES reception (id)
);

CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),

)