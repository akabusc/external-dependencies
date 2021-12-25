\connect training

CREATE TABLE data.reddit
(
    id     bigint NOT NULL,
    author text,
    body   text
);


ALTER TABLE data.reddit OWNER TO training_admin;

CREATE SEQUENCE data.reddit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE CACHE 1;


ALTER TABLE data.reddit_id_seq OWNER TO training_admin;

ALTER SEQUENCE data.reddit_id_seq OWNED BY data.reddit.id;