-- Table: dbt_source.features_ptnf

-- DROP TABLE IF EXISTS dbt_source.features_ptnf;

CREATE TABLE IF NOT EXISTS dbt_source.features_ptnf
(
    id bigint NOT NULL DEFAULT 'nextval('dbt_source.features_ptnf_id_seq'::regclass)',
    bfcid bigint,
    mls_number character varying(45) COLLATE pg_catalog."default",
    appliance text COLLATE pg_catalog."default",
    architecturestyle text COLLATE pg_catalog."default",
    attic text COLLATE pg_catalog."default",
    barbecuearea text COLLATE pg_catalog."default",
    basement text COLLATE pg_catalog."default",
    buildingunitcount text COLLATE pg_catalog."default",
    cableready text COLLATE pg_catalog."default",
    cellingfan text COLLATE pg_catalog."default",
    condofloornumber text COLLATE pg_catalog."default",
    coolingsystem text COLLATE pg_catalog."default",
    deck text COLLATE pg_catalog."default",
    disabledaccess text COLLATE pg_catalog."default",
    dock text COLLATE pg_catalog."default",
    doorman text COLLATE pg_catalog."default",
    doublepanelwindows text COLLATE pg_catalog."default",
    elevator text COLLATE pg_catalog."default",
    exteriortype text COLLATE pg_catalog."default",
    fencing text COLLATE pg_catalog."default",
    fireplace text COLLATE pg_catalog."default",
    floorcovering text COLLATE pg_catalog."default",
    garden text COLLATE pg_catalog."default",
    gatedentry text COLLATE pg_catalog."default",
    greenhouse text COLLATE pg_catalog."default",
    heatingfuel text COLLATE pg_catalog."default",
    heatingsystem text COLLATE pg_catalog."default",
    horseproperty text COLLATE pg_catalog."default",
    hottubspa text COLLATE pg_catalog."default",
    intercom text COLLATE pg_catalog."default",
    interior text COLLATE pg_catalog."default",
    jettedbathtub text COLLATE pg_catalog."default",
    lawn text COLLATE pg_catalog."default",
    laundary text COLLATE pg_catalog."default",
    legaldescription text COLLATE pg_catalog."default",
    motherinlaw text COLLATE pg_catalog."default",
    newcontruction text COLLATE pg_catalog."default",
    numfloors text COLLATE pg_catalog."default",
    numparkingspaces text COLLATE pg_catalog."default",
    parkingtype text COLLATE pg_catalog."default",
    patio text COLLATE pg_catalog."default",
    pond text COLLATE pg_catalog."default",
    pool text COLLATE pg_catalog."default",
    porch text COLLATE pg_catalog."default",
    rooftype text COLLATE pg_catalog."default",
    roomcount text COLLATE pg_catalog."default",
    rooms text COLLATE pg_catalog."default",
    rvparking text COLLATE pg_catalog."default",
    sauna text COLLATE pg_catalog."default",
    securitysystem text COLLATE pg_catalog."default",
    skylight text COLLATE pg_catalog."default",
    sportscourt text COLLATE pg_catalog."default",
    sprinklersystem text COLLATE pg_catalog."default",
    vaultedcelling text COLLATE pg_catalog."default",
    viewtype text COLLATE pg_catalog."default",
    water text COLLATE pg_catalog."default",
    waterfront text COLLATE pg_catalog."default",
    wetbar text COLLATE pg_catalog."default",
    wired text COLLATE pg_catalog."default",
    yearremodeled text COLLATE pg_catalog."default",
    zoning text COLLATE pg_catalog."default",
    taxyear text COLLATE pg_catalog."default",
    taxamount text COLLATE pg_catalog."default",
    addl_features text COLLATE pg_catalog."default",
    CONSTRAINT features_ptnf_pkey PRIMARY KEY (id),
    CONSTRAINT features_ptnf_bfcid_key UNIQUE (bfcid),
    CONSTRAINT features_ptnf_bfcid_fkey FOREIGN KEY (bfcid)
        REFERENCES dbt_source.property_ptnf (bfcid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS dbt_source.features_ptnf
    OWNER to postgres;



-- Table: dbt_source.media_ptnf

-- DROP TABLE IF EXISTS dbt_source.media_ptnf;

CREATE TABLE IF NOT EXISTS dbt_source.media_ptnf
(
    id bigint NOT NULL DEFAULT 'nextval('dbt_source.media_ptnf_id_seq'::regclass)',
    bfcid bigint NOT NULL,
    mls_number character varying(45) COLLATE pg_catalog."default",
    photo_type character varying(10) COLLATE pg_catalog."default",
    caption text COLLATE pg_catalog."default",
    url text COLLATE pg_catalog."default",
    photoorder integer,
    CONSTRAINT media_ptnf_pkey PRIMARY KEY (id),
    CONSTRAINT media_ptnf_bfcid_fkey FOREIGN KEY (bfcid)
        REFERENCES dbt_source.property_ptnf (bfcid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS dbt_source.media_ptnf
    OWNER to postgres;


    -- Table: dbt_source.property_ptnf

-- DROP TABLE IF EXISTS dbt_source.property_ptnf;

CREATE TABLE IF NOT EXISTS dbt_source.property_ptnf
(
    id bigint NOT NULL DEFAULT 'nextval('dbt_source.property_ptnf_id_seq'::regclass)',
    bfcid bigint NOT NULL,
    mls_number character varying(45) COLLATE pg_catalog."default",
    datasource character varying(50) COLLATE pg_catalog."default" NOT NULL,
    unit_number character varying(10) COLLATE pg_catalog."default",
    address character varying(60) COLLATE pg_catalog."default",
    city character varying(40) COLLATE pg_catalog."default",
    state character varying(2) COLLATE pg_catalog."default",
    zip character varying(10) COLLATE pg_catalog."default",
    county character varying(30) COLLATE pg_catalog."default",
    latitude double precision DEFAULT 0,
    longitude double precision DEFAULT 0,
    type character varying(100) COLLATE pg_catalog."default",
    subtype character varying(150) COLLATE pg_catalog."default",
    title character varying(100) COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    parcel_number character varying(50) COLLATE pg_catalog."default",
    beds real,
    baths real,
    fullbaths real,
    halfbaths real,
    areasqft character varying(45) COLLATE pg_catalog."default",
    lotsqft character varying(45) COLLATE pg_catalog."default",
    year_built character varying(4) COLLATE pg_catalog."default",
    display_address smallint DEFAULT 8,
    display_listing smallint DEFAULT 4,
    status character varying(30) COLLATE pg_catalog."default",
    saledate date,
    saleprice double precision,
    listdate date,
    orig_listprice double precision,
    curr_listprice double precision,
    days_on_market integer,
    date_price_adjust date,
    listing_url text COLLATE pg_catalog."default",
    vtour_url text COLLATE pg_catalog."default",
    modif_timestamp timestamp without time zone,
    expiry_date date,
    misc text COLLATE pg_catalog."default",
    photo_count integer,
    video_count integer,
    photo_modif_date timestamp without time zone,
    video_modif_date timestamp without time zone,
    dist_school character varying(60) COLLATE pg_catalog."default",
    elem_school character varying(60) COLLATE pg_catalog."default",
    midl_school character varying(60) COLLATE pg_catalog."default",
    high_school character varying(60) COLLATE pg_catalog."default",
    nabrhd_name character varying(150) COLLATE pg_catalog."default",
    nabrhd_desc text COLLATE pg_catalog."default",
    nearby_url text COLLATE pg_catalog."default",
    identifier character varying(255) COLLATE pg_catalog."default",
    geolevel integer,
    main_photo text COLLATE pg_catalog."default",
    price_change double precision,
    status_change character varying(30) COLLATE pg_catalog."default",
    broker_code character varying(45) COLLATE pg_catalog."default",
    broker_name character varying(150) COLLATE pg_catalog."default",
    office_listing_yn smallint,
    extra1 character varying(2) COLLATE pg_catalog."default",
    extra2 character varying(2) COLLATE pg_catalog."default",
    extra3 text COLLATE pg_catalog."default",
    extra4 character varying(2) COLLATE pg_catalog."default",
    extra5 character varying(2) COLLATE pg_catalog."default",
    postinguser_id bigint,
    CONSTRAINT property_ptnf_pkey PRIMARY KEY (bfcid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS dbt_source.property_ptnf
    OWNER to postgres;


    -- Table: dbt_source.user_ptnf

-- DROP TABLE IF EXISTS dbt_source.user_ptnf;

CREATE TABLE IF NOT EXISTS dbt_source.user_ptnf
(
    id bigint NOT NULL DEFAULT 'nextval('dbt_source.user_ptnf_id_seq'::regclass)',
    bfcid bigint NOT NULL,
    mls_number character varying(45) COLLATE pg_catalog."default",
    user_sourceid character varying(50) COLLATE pg_catalog."default" DEFAULT 'NULL::character varying',
    office_name character varying(150) COLLATE pg_catalog."default" DEFAULT 'NULL::character varying',
    fname character varying(45) COLLATE pg_catalog."default" DEFAULT 'NULL::character varying',
    email character varying(90) COLLATE pg_catalog."default" DEFAULT 'NULL::character varying',
    phone character varying(45) COLLATE pg_catalog."default" DEFAULT 'NULL::character varying',
    mobile character varying(45) COLLATE pg_catalog."default" DEFAULT 'NULL::character varying',
    user_code character varying(50) COLLATE pg_catalog."default" DEFAULT 'NULL::character varying',
    licence_no character varying(50) COLLATE pg_catalog."default" DEFAULT 'NULL::character varying',
    broker_type character varying(50) COLLATE pg_catalog."default" DEFAULT 'NULL::character varying',
    agent_type character varying(50) COLLATE pg_catalog."default" DEFAULT 'NULL::character varying',
    CONSTRAINT user_ptnf_pkey PRIMARY KEY (id),
    CONSTRAINT user_ptnf_bfcid_fkey FOREIGN KEY (bfcid)
        REFERENCES dbt_source.property_ptnf (bfcid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS dbt_source.user_ptnf
    OWNER to postgres;
