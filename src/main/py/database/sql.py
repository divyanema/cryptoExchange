-- Database: CryptoDB

-- DROP DATABASE "CryptoDB";

CREATE DATABASE "CryptoDB"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;


-- Table: public.crypto_user

-- DROP TABLE public.crypto_user;

CREATE TABLE public.crypto_user
(
    user_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    first_name character varying(50) COLLATE pg_catalog."default",
    last_name character varying(50) COLLATE pg_catalog."default",
    email character varying(100) COLLATE pg_catalog."default",
    pan_no character varying(20) COLLATE pg_catalog."default",
    dob date,
    mobile_no character varying(30) COLLATE pg_catalog."default",
    exchange_account_id character varying(30) COLLATE pg_catalog."default",
    status character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT "User_pkey" PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE public.crypto_user
    OWNER to postgres;


-- Table: public.crypto_wallet

-- DROP TABLE public.crypto_wallet;

CREATE TABLE public.crypto_wallet
(
    wallet_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    user_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    type character varying(100) COLLATE pg_catalog."default",
    balance numeric,
    updated_timestamp timestamp with time zone,
    status character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT crypto_wallet_pkey PRIMARY KEY (wallet_id),
    CONSTRAINT user_wallet_foreign_key FOREIGN KEY (user_id)
        REFERENCES public.crypto_user (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE public.crypto_wallet
    OWNER to postgres;