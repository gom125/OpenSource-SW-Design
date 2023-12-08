###############################
# Using Jsonb Version
#
# PK, PK data type, PK condition
PK_resources= ['ri', 'varchar(255)', 'PRIMARY KEY']
PK_identifiers = ['ri', 'varchar(255)', 'PRIMARY KEY']
PK_srn = ['ri', 'varchar(255)', 'PRIMARY KEY']
PK_children = ['ri', 'varchar(255)', 'PRIMARY KEY']
PK_subscriptions = ['ri', 'varchar(255)', 'PRIMARY KEY']
PK_statistics = ['id', 'serial', 'PRIMARY KEY']
PK_actions = ['ri', 'varchar(255)', 'PRIMARY KEY']
PK_batchNotifications = ['id', 'serial', 'PRIMARY KEY']
PK_requests = ['ts', 'real', 'PRIMARY KEY']
PK_schedules = ['ri', 'varchar(255)', 'PRIMARY KEY']


table_resources_query = """
CREATE TABLE IF NOT EXISTS resources (
	ri varchar(255) PRIMARY KEY,
    m2m_attr jsonb
);"""

table_identifiers_query = """
CREATE TABLE IF NOT EXISTS identifier (
	ri varchar(255) PRIMARY KEY,
	rn varchar(255),
	srn varchar(255),
	ty integer
);"""

table_srn_query = """
CREATE TABLE IF NOT EXISTS srn (
	srn varchar(255) PRIMARY KEY,
	ri varchar(255)
);"""

table_children_query = """
CREATE TABLE IF NOT EXISTS children (
	ri varchar(255) PRIMARY KEY,
	ch varchar(255)[]
);"""

table_subscriptions_query = """
CREATE TABLE IF NOT EXISTS subscriptions (
	ri varchar(255) PRIMARY KEY,
	nct integer,
	net integer[],
	atr varchar(255)[],
	chty integer[],
	exc integer,
	ln boolean,
	nus varchar(255)[],
	bn text,
	cr varchar(255),
	nec integer,
	org varchar(255),
	ma varchar(255),
	nse boolean
);"""

table_statistics_query = """
CREATE TABLE IF NOT EXISTS statistics (
	id serial PRIMARY KEY,
	eve jsonb
);"""

table_actions_query = """
CREATE TABLE IF NOT EXISTS actions (
	ri varchar(255) PRIMARY KEY,
	subject varchar(255),
	apy integer,
	evm integer,
	evc text,
	ecp integer,
	periodTS varchar(255),
	count integer
);"""

table_batchNotifications_query = """
CREATE TABLE IF NOT EXISTS batchnotifications (
	id serial PRIMARY KEY,
	ri varchar(255),
	nu varchar(255),
	tstamp timstamp,
	request text
);"""

table_requests_query = """
CREATE TABLE IF NOT EXISTS requests (
	ri varchar(255),
	srn varchar(255),
	ts real PRIMARY KEY,
	org varchar(255),
	op text,
	rsc text,
	out boolean,
	ot varchar(255),
	req jsonb,
	rsp jsonb
);"""

table_schedules_query = """
CREATE TABLE IF NOT EXISTS schedules (
	ri varchar(255) PRIMARY KEY,
	pi varchar(255),
	sce varchar(255)[]
);"""

###############################
# Seperate database Version
# schema - (database table name)
# table - (database table's columns name)
# column - (database table's columns name)
# value - (database table's columns's value)

schema_resources_query = """
CREATE TABLE IF NOT EXISTS resources.ri (
	ri varchar(255) PRIMARY KEY
);"""

schema_identifiers_query = """
CREATE TABLE IF NOT EXISTS identifiers.ri (
	ri varchar(255) PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS identifiers.rn (
	ri varchar(255),
    rn varchar(255),
    FOREIGN KEY (ri) REFERENCES identifiers.ri(ri)
);
CREATE TABLE IF NOT EXISTS identifiers.srn (
	ri varchar(255),
	srn varchar(255),
    FOREIGN KEY (ri) REFERENCES identifiers.ri(ri)
);
CREATE TABLE IF NOT EXISTS identifiers.ty (
	ri varchar(255),
	ty integer,
    FOREIGN KEY (ri) REFERENCES identifiers.ri(ri)
);"""

schema_srn_query = """
CREATE TABLE IF NOT EXISTS srn.srn (
	srn varchar(255) PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS srn.ri (
	srn varchar(255),
	ri varchar(255),
    FOREIGN KEY (srn) REFERENCES srn.srn(srn)
);"""

schema_children_query = """
CREATE TABLE IF NOT EXISTS children.ri (
	ri varchar(255) PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS children.ch (
	ri varchar(255),
	ch varchar(255)[],
    FOREIGN KEY (ri) REFERENCES children.ri(ri)
);"""

schema_subscriptions_query = """
CREATE TABLE IF NOT EXISTS subscriptions.ri (
	ri varchar(255) PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS subscriptions.nct (
	ri varchar(255),
	nct integer,
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.net (
	ri varchar(255),
	net integer[],
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.atr (
	ri varchar(255) ,
	atr varchar(255)[],
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.chty (
	ri varchar(255),
	chty integer[],
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.exc (
	ri varchar(255),
	exc integer,
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.ln (
	ri varchar(255),
	ln boolean,
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.nus (
	ri varchar(255),
	nus varchar(255)[],
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.bn (
	ri varchar(255),
	bn text,
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.cr (
	ri varchar(255),
	cr varchar(255),
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.nec (
	ri varchar(255),
	nec integer,
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.org (
	ri varchar(255),
	org varchar(255),
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.ma (
	ri varchar(255),
	ma varchar(255),
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);
CREATE TABLE IF NOT EXISTS subscriptions.nse (
	ri varchar(255),
	nse boolean,
    FOREIGN KEY (ri) REFERENCES subscriptions.ri(ri)
);"""

schema_statistics_query = """
CREATE TABLE IF NOT EXISTS statistics.id (
	id serial PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS statistics.eve (
	id serial,
	eve jsonb,
    FOREIGN KEY (id) REFERENCES statistics.id(id)
);"""

schema_actions_query = """
CREATE TABLE IF NOT EXISTS actions.ri (
	ri varchar(255) PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS actions.subject (
	ri varchar(255),
	subject varchar(255),
	FOREIGN KEY (ri) REFERENCES actions.ri(ri)
);
CREATE TABLE IF NOT EXISTS actions.apy (
	ri varchar(255),
	apy integer,
	FOREIGN KEY (ri) REFERENCES actions.ri(ri)
);
CREATE TABLE IF NOT EXISTS actions.evm (
	ri varchar(255),
	evm integer,
	FOREIGN KEY (ri) REFERENCES actions.ri(ri)
);
CREATE TABLE IF NOT EXISTS actions.evc (
	ri varchar(255),
	evc text,
	FOREIGN KEY (ri) REFERENCES actions.ri(ri)
);
CREATE TABLE IF NOT EXISTS actions.ecp (
	ri varchar(255),
	ecp integer,
	FOREIGN KEY (ri) REFERENCES actions.ri(ri)
);
CREATE TABLE IF NOT EXISTS actions.periodTS (
	ri varchar(255),
	periodTS varchar(255),
	FOREIGN KEY (ri) REFERENCES actions.ri(ri)
);
CREATE TABLE IF NOT EXISTS actions.count (
	ri varchar(255),
	count integer,
	FOREIGN KEY (ri) REFERENCES actions.ri(ri)
);"""

schema_batchNotifications_query = """
CREATE TABLE IF NOT EXISTS batchnotifications.id (
	id serial PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS batchnotifications.ri (
	id serial,
	ri varchar(255),
	FOREIGN KEY (id) REFERENCES batchnotifications.id(id)
);
CREATE TABLE IF NOT EXISTS batchnotifications.nu (
	id serial,
	nu varchar(255),
	FOREIGN KEY (id) REFERENCES batchnotifications.id(id)
);
CREATE TABLE IF NOT EXISTS batchnotifications.tstamp (
	id serial,
	tstamp varchar(255),
	FOREIGN KEY (id) REFERENCES batchnotifications.id(id)
);
CREATE TABLE IF NOT EXISTS batchnotifications.request (
	id serial,
	request text,
	FOREIGN KEY (id) REFERENCES batchnotifications.id(id)
);"""

schema_requests_query = """
CREATE TABLE IF NOT EXISTS requests.ts (
	ts real PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS requests.ri (
	ts real,
	ri varchar(255),
	FOREIGN KEY (ts) REFERENCES requests.ts(ts)
);
CREATE TABLE IF NOT EXISTS requests.srn (
	ts real,
	srn varchar(255),
	FOREIGN KEY (ts) REFERENCES requests.ts(ts)
);
CREATE TABLE IF NOT EXISTS requests.org (
	ts real,
	org varchar(255),
	FOREIGN KEY (ts) REFERENCES requests.ts(ts)
);
CREATE TABLE IF NOT EXISTS requests.op (
	ts real,
	op text,
	FOREIGN KEY (ts) REFERENCES requests.ts(ts)
);
CREATE TABLE IF NOT EXISTS requests.rsc (
	ts real,
	rsc text,
	FOREIGN KEY (ts) REFERENCES requests.ts(ts)
);
CREATE TABLE IF NOT EXISTS requests.out (
	ts real,
	out boolean,
	FOREIGN KEY (ts) REFERENCES requests.ts(ts)
);
CREATE TABLE IF NOT EXISTS requests.ot (
	ts real,
	ot varchar(255),
	FOREIGN KEY (ts) REFERENCES requests.ts(ts)
);
CREATE TABLE IF NOT EXISTS requests.req (
	ts real,
	req jsonb,
	FOREIGN KEY (ts) REFERENCES requests.ts(ts)
);
CREATE TABLE IF NOT EXISTS requests.rsp (
	ts real,
	rsp jsonb,
	FOREIGN KEY (ts) REFERENCES requests.ts(ts)
);"""

schema_schedules_query = """
CREATE TABLE IF NOT EXISTS schedules.ri (
	ri varchar(255) PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS schedules.pi (
	ri varchar(255),
	pi varchar(255),
	FOREIGN KEY (ri) REFERENCES schedules.ri(ri)
);
CREATE TABLE IF NOT EXISTS schedules.sce (
	ri varchar(255),
	sce varchar(255)[],
	FOREIGN KEY (ri) REFERENCES schedules.ri(ri)
);"""