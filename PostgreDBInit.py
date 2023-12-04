
resources_query = """
CREATE TABLE IF NOT EXISTS resources (
	ri varchar(255) PRIMARY KEY,
    m2m_attr jsonb
);"""

identifiers_query = """
CREATE TABLE IF NOT EXISTS identifier (
	ri varchar(255) PRIMARY KEY,
	rn varchar(255),
	srn varchar(255),
	ty integer
);"""

srn_query = """
CREATE TABLE IF NOT EXISTS srn (
	srn varchar(255) PRIMARY KEY,
	ri varchar(255)
);"""

children_query = """
CREATE TABLE IF NOT EXISTS children (
	ri varchar(255) PRIMARY KEY,
	ch varchar(255)[]
);"""

subscriptions_query = """
CREATE TABLE IF NOT EXISTS subsripttions (
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

statistics_query = """
CREATE TABLE IF NOT EXISTS statistics (
	eve jsonb
);"""

actions_query = """
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

batchNotifications_query = """
CREATE TABLE IF NOT EXISTS batchNotifications (
	ri varchar(255),
	nu varchar(255),
	tstamp varchar(255),
	request text
);"""

requests_query = """
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

schedules_query = """
CREATE TABLE IF NOT EXISTS schedules (
	ri varchar(255) PRIMARY KEY,
	pi varchar(255),
	sce varchar(255)[]
);"""

