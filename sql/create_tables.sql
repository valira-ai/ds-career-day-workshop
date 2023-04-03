-- bed type
CREATE TABLE IF NOT EXISTS public.bedtype
(
    bed_type_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    bed_type_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT bed_type_pkey PRIMARY KEY (bed_type_id),
    CONSTRAINT bed_type_unique UNIQUE (bed_type_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bedtype
    OWNER to postgres;
	
	
-- cancellation policy
CREATE TABLE IF NOT EXISTS public.cancelpolicy
(
    cancel_policy_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    cancel_policy_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT cancel_policy_pkey PRIMARY KEY (cancel_policy_id),
    CONSTRAINT cancel_policy_unique UNIQUE (cancel_policy_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.cancelpolicy
    OWNER to postgres;
	
	
-- city
CREATE TABLE IF NOT EXISTS public.city
(
    city_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    city_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    center_longitude numeric NOT NULL,
    center_latitude numeric NOT NULL,
    CONSTRAINT city_pkey PRIMARY KEY (city_id),
    CONSTRAINT city_unique UNIQUE (city_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.city
    OWNER to postgres;
	
	
-- listing
CREATE TABLE IF NOT EXISTS public.listing
(
    listing_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    city_id integer NOT NULL,
    room_type_id integer NOT NULL,
    neighbourhood_id integer NOT NULL,
    longitude numeric NOT NULL,
    latitude numeric NOT NULL,
    price money NOT NULL,
    minimum_nights integer NOT NULL,
    listing_given_id bigint NOT NULL,
    property_type_id bigint NOT NULL,
    accommodates integer NOT NULL,
    bathrooms integer NOT NULL,
    bedrooms integer NOT NULL,
    beds integer NOT NULL,
    bed_type_id integer NOT NULL,
    cancel_policy_id integer NOT NULL,
    features character varying COLLATE pg_catalog."default",
    amenities character varying COLLATE pg_catalog."default",
    CONSTRAINT listing_pkey PRIMARY KEY (listing_id),
    CONSTRAINT listing_unique UNIQUE (listing_given_id),
    CONSTRAINT "FK_bedtype" FOREIGN KEY (bed_type_id)
        REFERENCES public.bedtype (bed_type_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "FK_cancelpolicy" FOREIGN KEY (cancel_policy_id)
        REFERENCES public.cancelpolicy (cancel_policy_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "FK_city" FOREIGN KEY (city_id)
        REFERENCES public.city (city_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "FK_neighbourhood" FOREIGN KEY (neighbourhood_id)
        REFERENCES public.neighbourhood (neighbourhood_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "FK_propertytype" FOREIGN KEY (property_type_id)
        REFERENCES public.propertytype (property_type_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "FK_roomtype" FOREIGN KEY (room_type_id)
        REFERENCES public.roomtype (room_type_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.listing
    OWNER to postgres;
	
	
-- neighbourhood
CREATE TABLE IF NOT EXISTS public.neighbourhood
(
    neighbourhood_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    neighbourhood_name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT neighbourhood_pkey PRIMARY KEY (neighbourhood_id),
    CONSTRAINT neighbourhood_unique UNIQUE (neighbourhood_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.neighbourhood
    OWNER to postgres;


-- property type
CREATE TABLE IF NOT EXISTS public.propertytype
(
    property_type_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    property_type_name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT propertytype_pkey PRIMARY KEY (property_type_id),
    CONSTRAINT propertytype_unique UNIQUE (property_type_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.propertytype
    OWNER to postgres;
	
	
-- raw
CREATE TABLE IF NOT EXISTS public."raw"
(
    neighbourhood character varying COLLATE pg_catalog."default",
    latitude numeric,
    longitude numeric,
    room_type character varying COLLATE pg_catalog."default",
    price numeric,
    minimum_nights integer,
    id bigint,
    city character varying COLLATE pg_catalog."default",
    accommodates integer,
    bathrooms integer,
    bedrooms integer,
    beds integer,
    bed_type character varying COLLATE pg_catalog."default",
    cancel_policy character varying COLLATE pg_catalog."default",
    features character varying COLLATE pg_catalog."default",
    amenities character varying COLLATE pg_catalog."default",
    property_type character varying COLLATE pg_catalog."default",
    CONSTRAINT raw_unique UNIQUE (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."raw"
    OWNER to postgres;
	
	
-- room type
CREATE TABLE IF NOT EXISTS public.roomtype
(
    room_type_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    room_type_name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT roomtype_pkey PRIMARY KEY (room_type_id),
    CONSTRAINT roomtype_unique UNIQUE (room_type_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.roomtype
    OWNER to postgres;