CREATE TABLE sample_plate (
    sample_plate_id character varying(40) NOT NULL,
    type_id character varying(40) NOT NULL,
    date_created timestamp without time zone,
    name character varying(100) NOT NULL,
    description character varying(2048),
    external_barcode character varying(100),
    status enum_sample_plate_status NOT NULL,
    operator_id character varying(10),
    storage_location_id character varying(40) NOT NULL
);

CREATE TABLE sample_plate_layout (
    sample_plate_id character varying(40) NOT NULL,
    well_id integer NOT NULL,
    sample_id character varying(40) NOT NULL,
    "row" character varying(10),
    "column" integer,
    date_created timestamp without time zone,
    operator_id character varying(10),
    notes character varying(512),
    status enum_sample_status NOT NULL
);

CREATE TABLE sample_plate_type (
    type_id character varying(40) NOT NULL,
    name character varying(100),
    description character varying(2048),
    reference_pdf_name character varying(255),
    reference_thumbnail_name character varying(255),
    number_clusters integer NOT NULL,
    sample_plate_type enum_sample_plate_type NOT NULL,
    status enum_sample_plate_type_status NOT NULL,
    rows_alpha character varying(100),
    cols_num integer
);

CREATE TABLE sample_type (
    type_id character varying(40) NOT NULL,
    id_prefix character varying(40),
    name character varying(100),
    description character varying(2048),
    status enum_sample_type_status NOT NULL
);

CREATE TABLE sample (
    sample_id character varying(40) NOT NULL,
    type_id character varying(40) NOT NULL,
    date_created timestamp without time zone,
    operator_id character varying(10),
    name character varying(100) NOT NULL,
    description character varying(1024),
    external_barcode character varying(100),
    parent_process_id character varying(40),
    parent_transfer_process_id character varying(40),
    status enum_sample_status NOT NULL,
    fwd_primer_ps_id character varying(40),
    rev_primer_ps_id character varying(40),
    reagent_type_set_lot_id character varying(40)
);

CREATE TABLE operator (
    operator_id character varying(10) NOT NULL,
    jira_username character varying(100),
    email character varying(120) NOT NULL,
    user_id character varying(80) NOT NULL,
    first_name character varying(80),
    middle_initial character varying(1),
    last_name character varying(80),
    role integer,
    last_seen timestamp without time zone,
    initials character varying(10),
    ip_addr character varying(20),
    login_count integer
);

CREATE TABLE storage_location (
    storage_location_id character varying(40) NOT NULL,
    parent_storage_location_id character varying(40),
    name character varying(100),
    description character varying(2048),
    location_type enum_storage_location_type NOT NULL,
    status enum_storage_status NOT NULL
);

