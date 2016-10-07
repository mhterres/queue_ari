--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.0
-- Dumped by pg_dump version 9.6.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP INDEX IF EXISTS public.idx_queues_name;
DROP INDEX IF EXISTS public.idx_queues_id;
DROP INDEX IF EXISTS public.idx_queue_members_queues_id;
DROP INDEX IF EXISTS public.idx_queue_members_queue_name;
DROP INDEX IF EXISTS public.idx_queue_members_interface;
DROP TABLE IF EXISTS public.queues;
DROP SEQUENCE IF EXISTS public.queues_id_seq;
DROP TABLE IF EXISTS public.queue_rules;
DROP TABLE IF EXISTS public.queue_members;
DROP TYPE IF EXISTS public.yesno_values;
DROP TYPE IF EXISTS public.yes_no_values;
DROP TYPE IF EXISTS public.queue_strategy_values;
DROP TYPE IF EXISTS public.queue_member_type_values;
DROP TYPE IF EXISTS public.queue_autopause_values;
DROP EXTENSION IF EXISTS plpgsql;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: queue_autopause_values; Type: TYPE; Schema: public; Owner: queue_ari
--

CREATE TYPE queue_autopause_values AS ENUM (
    'yes',
    'no',
    'all'
);


ALTER TYPE queue_autopause_values OWNER TO queue_ari;

--
-- Name: queue_member_type_values; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE queue_member_type_values AS ENUM (
    'fixed',
    'dynamic'
);


ALTER TYPE queue_member_type_values OWNER TO postgres;

--
-- Name: queue_strategy_values; Type: TYPE; Schema: public; Owner: queue_ari
--

CREATE TYPE queue_strategy_values AS ENUM (
    'ringall',
    'leastrecent',
    'fewestcalls',
    'random',
    'rrmemory',
    'linear',
    'wrandom',
    'rrordered'
);


ALTER TYPE queue_strategy_values OWNER TO queue_ari;

--
-- Name: yes_no_values; Type: TYPE; Schema: public; Owner: queue_ari
--

CREATE TYPE yes_no_values AS ENUM (
    'yes',
    'no'
);


ALTER TYPE yes_no_values OWNER TO queue_ari;

--
-- Name: yesno_values; Type: TYPE; Schema: public; Owner: queue_ari
--

CREATE TYPE yesno_values AS ENUM (
    'yes',
    'no'
);


ALTER TYPE yesno_values OWNER TO queue_ari;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: queue_members; Type: TABLE; Schema: public; Owner: queue_ari
--

CREATE TABLE queue_members (
    queues_id bigint NOT NULL,
    type queue_member_type_values NOT NULL,
    queue_name character varying(80) NOT NULL,
    interface character varying(80) NOT NULL,
    membername character varying(80),
    state_interface character varying(80),
    penalty integer,
    paused integer,
    uniqueid integer NOT NULL
);


ALTER TABLE queue_members OWNER TO queue_ari;

--
-- Name: queue_rules; Type: TABLE; Schema: public; Owner: queue_ari
--

CREATE TABLE queue_rules (
    rule_name character varying(80) NOT NULL,
    "time" character varying(32) NOT NULL,
    min_penalty character varying(32) NOT NULL,
    max_penalty character varying(32) NOT NULL
);


ALTER TABLE queue_rules OWNER TO queue_ari;

--
-- Name: queues_id_seq; Type: SEQUENCE; Schema: public; Owner: queue_ari
--

CREATE SEQUENCE queues_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 1000000
    CACHE 1;


ALTER TABLE queues_id_seq OWNER TO queue_ari;

--
-- Name: queues; Type: TABLE; Schema: public; Owner: queue_ari
--

CREATE TABLE queues (
    id bigint DEFAULT nextval('queues_id_seq'::regclass) NOT NULL,
    name character varying(128) NOT NULL,
    musiconhold character varying(128),
    announce character varying(128),
    context character varying(128),
    timeout integer,
    ringinuse yesno_values,
    setinterfacevar yesno_values,
    setqueuevar yesno_values,
    setqueueentryvar yesno_values,
    monitor_format character varying(8),
    membermacro character varying(512),
    membergosub character varying(512),
    queue_youarenext character varying(128),
    queue_thereare character varying(128),
    queue_callswaiting character varying(128),
    queue_quantity1 character varying(128),
    queue_quantity2 character varying(128),
    queue_holdtime character varying(128),
    queue_minutes character varying(128),
    queue_minute character varying(128),
    queue_seconds character varying(128),
    queue_thankyou character varying(128),
    queue_callerannounce character varying(128),
    queue_reporthold character varying(128),
    announce_frequency integer,
    announce_to_first_user yesno_values,
    min_announce_frequency integer,
    announce_round_seconds integer,
    announce_holdtime character varying(128),
    announce_position character varying(128),
    announce_position_limit integer,
    periodic_announce character varying(50),
    periodic_announce_frequency integer,
    relative_periodic_announce yesno_values,
    random_periodic_announce yesno_values,
    retry integer,
    wrapuptime integer,
    penaltymemberslimit integer,
    autofill yesno_values,
    monitor_type character varying(128),
    autopause queue_autopause_values,
    autopausedelay integer,
    autopausebusy yesno_values,
    autopauseunavail yesno_values,
    maxlen integer,
    servicelevel integer,
    strategy queue_strategy_values,
    joinempty character varying(128),
    leavewhenempty character varying(128),
    reportholdtime yesno_values,
    memberdelay integer,
    weight integer,
    timeoutrestart yesno_values,
    defaultrule character varying(128),
    timeoutpriority character varying(128)
);


ALTER TABLE queues OWNER TO queue_ari;

--
-- Name: idx_queue_members_interface; Type: INDEX; Schema: public; Owner: queue_ari
--

CREATE INDEX idx_queue_members_interface ON queue_members USING btree (interface);


--
-- Name: idx_queue_members_queue_name; Type: INDEX; Schema: public; Owner: queue_ari
--

CREATE INDEX idx_queue_members_queue_name ON queue_members USING btree (queue_name);


--
-- Name: idx_queue_members_queues_id; Type: INDEX; Schema: public; Owner: queue_ari
--

CREATE INDEX idx_queue_members_queues_id ON queue_members USING btree (queues_id);


--
-- Name: idx_queues_id; Type: INDEX; Schema: public; Owner: queue_ari
--

CREATE UNIQUE INDEX idx_queues_id ON queues USING btree (id);


--
-- Name: idx_queues_name; Type: INDEX; Schema: public; Owner: queue_ari
--

CREATE UNIQUE INDEX idx_queues_name ON queues USING btree (name);


--
-- PostgreSQL database dump complete
--

