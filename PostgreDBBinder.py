
"""
    Query:        
        하위 파일:
            .
            ex) 스키마.테이블
                테이블.컬럼
        종료:
            ;
        트랜잭션:
            begin; end;
        create:
            User:
                CREATE USER {user_name} PASSWORD {password}
            SUPER User:
                CREATE USER {user_name} PASSWORD {password} SUPERUSER
            권한 부여 ALTER에 있음

            Database:
                CREATE DATABASE {database_name}
            
            TABLE: ({schema_name}. 생략시 public으로 자동 설정)
                CREATE TABLE {schema_name}.{table_name} (
                    {field_name1} {field_type} {condition},
                    {field_name2} {field_type} {condition},
                    ...
                )

        insert: row 행 추가
            INSERT INTO {schema_name}.{table_name}({column1}, {column2}, ...) VALUES ({value1}, {value2}, ...)
            value:str
            ex: '1', '{"ri":"19011000", "srn":123456779"}'
        
        update: row 행 수정
            UPDATE {schema_name}.{table_name} set {column_name} = '{value}' where {condition}

        upsert: insert + update

        select: 
            SELECT {column_name} FROM {schema_name}.{table_name} WHERE {condition} order by {column_name2} desc/asc
            condition: {condition} AND {condition} OR {condition} ...
            order by desc(내림차순), asc(오름차순)으로 출력

            table:
                SELECT * FROM {schema_name}.{table_name}
            column:
                SELECT {column1}, {column2}, ... FROM {schema_name}.{table_name}

        delete:
            DELETE FROM {schema_name}.{table_name} WHERE {condition}

        alter:
            Autho        

            table name:
                ALTER TABLE {schema_name}.{table_name} RENAME TO {renamed_table}
            column name:
                ALTER TABLE {schema_name}.{table_name} RENAME COLUMN {column_name} to {renamed_column}
            data type:
                    ALTER {schema_name}.{table_name} ALTER COLUMN {column_name} TYPE {data_type} 


        #=================================#
        데이터 베이스 확인: \l
            SELECT * FROM pg_catalog.pg_namespace;
        스키마 확인: \dn
            SELECT * FROM_catalog.pg_tables;
        #=================================#
"""

import psycopg
from psycopg.pq import Escaping
from psycopg.types.json import Jsonb
from psycopg import sql

import datetime
#import psycopg2
#import json
from PostgreDBInit import *
#from Storage import *

# Constants for database and table names
_resources = 'resources'
_identifiers = 'identifiers'
_srn = "srn"
_children = 'children'
_subscriptions = 'subscriptions'
_statistics = 'statistics'
_actions = 'actions'
_batchNotifications = 'batchnotifications'
_requests = 'requests'
_schedules = 'schedules'

class PostgreDBBinding():
    __slots__ = (
        # For Connect PostgreSQL DB Server
        'host', 
        'dbname', 
        'user', 
        'password',
        'port',
        # Connect and Control
        'conn',
        'cur',
        # Create
        'data',
        'json_data',
        'schema_name',
        'table_name',
        'values',
        'columns',
		# acme와 연결하기 위한 경로 및 초기 설정
        # PostgreSQL에 비슷한 용도로는 Shared Buffer가 사용됨
        # 분석 및 논의 필요
		'path',
		'cacheSize',    # TinyDB에서 쿼리를 캐시에 저장할 크기
		'writeDelay',
		'maxRequests',
		# 동기화 문제를 위한 초기 설정
        # PostgreSQL 테이블 Lock 문제 논의 필요
        # PostgreSQL은 db에 연결하기 때문.
		'lockResources',
		'lockIdentifiers',
		'lockChildResources',
		'lockStructuredIDs',
		'lockSubscriptions',
		'lockBatchNotifications',
		'lockStatistics',
		'lockActions',
		'lockRequests',
		'lockSchedules',
		# json 파일 for PostgreSQL
		'fileResources',
		'fileIdentifiers',
		'fileSubscriptions',
		'fileBatchNotifications',
		'fileStatistics',
		'fileActions',
		'fileRequests',
		'fileSchedules',
		# ACME 리소스
		'dbResources',
		'dbIdentifiers', 		
		'dbSubscriptions', 	
		'dbBatchNotifications',
		'dbStatistics',
		'dbActions',	
        'dbRequests',	
        'dbSchedules',	    
		# 테이블 생성
		'tabResources',
		'tabIdentifiers',
		'tabChildResources',
		'tabStructuredIDs',
		'tabSubscriptions',
		'tabBatchNotifications',
		'tabStatistics',
		'tabActions',
		'tabRequests',
		# TinyDB 쿼리문
		'resourceQuery',
		'identifierQuery',
		'subscriptionQuery',
		'batchNotificationQuery',
		'actionsQuery',
		'requestsQuery',
		'schedulesQuery',
	)

    # Connect PostgresDB 
    def __init__(
            self, 
            #path:str, 
            #postfix:str, 
            host='localhost', 
            dbname='acme', 
            user='postgres', 
            password='post1234', 
            port=5432
            ):
        
        """	Initialize the TinyDB binding.
		
			Args:
				path: Path to the database directory.
				postfix: Postfix for the database file names.
                host: database host address (defaults to UNIX socket if not provided)
                dbname: Storage's table name
                user: user name used to authenticate (defaults to postgres if not provided)
                password: password used to authenticate
                port: connection port number (defaults to 5432 if not provided)
        """

        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        '''
        # create transaction locks
        self.lockResources				= Lock()
        """ Lock for the resources table."""
        self.lockIdentifiers			= Lock()
        """ Lock for the identifiers table."""
        self.lockChildResources			= Lock()
        """ Lock for the childResources table."""
        self.lockStructuredIDs			= Lock()
        """ Lock for the structuredIDs table."""
        self.lockSubscriptions			= Lock()
        """ Lock for the subscriptions table."""
        self.lockBatchNotifications		= Lock()
        """ Lock for the batchNotifications table."""
        self.lockStatistics 			= Lock()
        """ Lock for the statistics table."""
        self.lockActions 				= Lock()
        """ Lock for the actions table."""
        self.lockRequests 				= Lock()
        """ Lock for the requests table."""
        self.lockSchedules 				= Lock()
        """ Lock for the schedules table."""'''

        try:
            self.conn = psycopg.connect(autocommit=True, host=self.host, dbname=self.dbname, user=self.user, password=self.password, port=self.port)
        except Exception as e:
            print(e)
            """Database is not exist"""
            self.conn = psycopg.connect(autocommit=True, host=self.host, dbname='postgres', user=self.user, password=self.password, port=self.port)
            self.cur = self.conn.cursor()
            """Connect Postgre DB as master user"""   
            self.Create_Database(self.dbname)
            self.conn = psycopg.connect(autocommit=True, host=self.host, dbname=self.dbname, user=self.user, password=self.password, port=self.port)
            """Create and Connect the Postgre DB"""
            self.cur = self.conn.cursor()
        else:
            self.cur = self.conn.cursor()

        # The database structure that handles data in a bundled manner using the JSONB data type.
        # Schema:Public - Table: database table
        All_jsonb = False
        if All_jsonb == True :
            # Create tables
            # PostgreDBInit
            self.PostgreTABLE(query=table_resources_query)
            self.PostgreTABLE(query=table_identifiers_query)
            self.PostgreTABLE(query=table_srn_query)
            self.PostgreTABLE(query=table_children_query)
            self.PostgreTABLE(query=table_subscriptions_query)
            self.PostgreTABLE(query=table_statistics_query)
            self.PostgreTABLE(query=table_actions_query)
            self.PostgreTABLE(query=table_batchNotifications_query)
            self.PostgreTABLE(query=table_requests_query)
            self.PostgreTABLE(query=table_schedules_query)
        # Schema: database table -> Table: resource.dict's key 
        # -> columns: resource.dict's key -> value: resource.dict's value  
        else :
            # Create Schema
            self.PostgreSCHEMA(schema_name=_resources)
            self.PostgreSCHEMA(schema_name=_identifiers)
            self.PostgreSCHEMA(schema_name=_srn)
            self.PostgreSCHEMA(schema_name=_children)
            self.PostgreSCHEMA(schema_name=_subscriptions)
            self.PostgreSCHEMA(schema_name=_statistics)
            self.PostgreSCHEMA(schema_name=_actions)
            self.PostgreSCHEMA(schema_name=_batchNotifications)
            self.PostgreSCHEMA(schema_name=_requests)
            self.PostgreSCHEMA(schema_name=_schedules)
            # Create Table
            self.PostgreTABLE(query=schema_resources_query)
            self.PostgreTABLE(query=schema_identifiers_query)
            self.PostgreTABLE(query=schema_srn_query)
            self.PostgreTABLE(query=schema_children_query)
            self.PostgreTABLE(query=schema_subscriptions_query)
            self.PostgreTABLE(query=schema_statistics_query)
            self.PostgreTABLE(query=schema_actions_query)
            self.PostgreTABLE(query=schema_batchNotifications_query)
            self.PostgreTABLE(query=schema_requests_query)
            self.PostgreTABLE(query=schema_schedules_query)

    # Terminate PostgreSQL DB Connection
    def __del__(self):
        self.cur.close()
        self.conn.close()

    # psycopg's wrapper function (execute)
    # msg is what your initial query or operation 
    # SELECT, UPDATE, CREATE, ...
    def execute(self, query, msg=""):
        try:
            self.cur.execute(query)

            is_select = msg.upper().startswith('SELECT')
            result = None

            if is_select:
                result = self.cur.fetchall()
            else:
                self.conn.commit()
            
            return result
        except Exception as e:
            print(f"Error Occured in {msg} Data!", e)
            #print("query is", query.as_string(self.conn))


    # create
    # CREATE DATABASE {database_name}
    # CREATE TABLE {table_name}
    def create(self, query):
        self.execute(query, 'CREATE')

    # insert
    # INSERT INTO {schema_name}.{table_name}({column1}, {column2}, ...) VALUES ({value1}, {value2}, ...)
    def insert(self, schema_name, table_name, columns, values):
        query = sql.SQL("INSERT INTO {field}.{table}({column}) VALUES({value});").format(
                field=sql.Identifier(schema_name),
                table=sql.Identifier(table_name),
                column=sql.SQL(', ').join(map(sql.Identifier, columns)),
                value=sql.SQL(', ').join(map(sql.Literal, values))
            )
        print(query.as_string(self.conn))
        self.execute(query=query, msg="INSERT")

    def update(self, schema_name, table_name, column, value, PK, PK_value):
            query = sql.SQL("UPDATE {schema}.{table} SET {column}={value} where {PK} = {PK_value};").format(
                    schema=sql.Identifier(schema_name),
                    table=sql.Identifier(table_name),
                    column=sql.Identifier(column),
                    value=sql.Literal(value),
                    PK=sql.Identifier(PK),
                    PK_value=sql.Literal(PK_value)
            )

            print(query.as_string(self.conn))
            self.execute(query, "UPDATE")
        
            """    # update
                def update(self, schema_name, table_name, columns, values, conditions, query):
                    query = sql.SQL("UPDATE {schema}.{table} SET {column} = {value} where %s").format(
                        schema=sql.Identifier(schema_name),
                        table=sql.Identifier(table_name),
                        column=sql.Identifier(columns),
                        value=sql.Literal(values),
                        condition=sql.Literal(conditions)
                    )
                    self.execute(query=query, msg="UPDATE")
            """
    # upsert
    def upsert(self, schema_name, table_name, column, value, update_value, PK):
        query = sql.SQL("INSERT INTO {schema}.{table} ({column}) VALUES ({value}) ON CONFLICT ({pk}) DO UPDATE SET {column}={new_val};").format(
                schema=sql.Identifier(schema_name),
                table=sql.Identifier(table_name),
                column=sql.Identifier(column),
                value=sql.Literal(value),
                new_val=sql.Literal(update_value),
                pk=sql.Identifier(PK),
        )

        print(query.as_string(self.conn))
        self.execute(query=query, msg="UPSERT")
    
    def search(self, table_name, condition, schema_name="public"):
        query= sql.SQL()

    # Create Database
    def Create_Database(self, dbname):
        query = sql.SQL("CREATE DATABASE {database};").format(database=sql.Identifier(dbname))
        self.execute(query, 'CREATE')
        """Create Database"""

    def Create_Schema(self, schema_name):
        query = sql.SQL("CREATE SCHEMA {schema};").format(schema=sql.Identifier(schema_name))
        self.execute(query, 'CREATE')
    
    # Create a table by the design of the database 
    # First column is FK(PK of ACME's database table)
    # If second column's data type is dict:
    #   Second column is PK
    #  
    #
    def Create_Table(self, schema_name, table_name, PK_column, PK_type, PK_condition, column, data_type, condition):
        query_table = sql.SQL("CREATE TABLE {schema_table} ( ").format(
            schema_table=sql.Identifier(schema_name, table_name),
        )
        query_column1 = sql.SQL("{column} {data_type} {condition}, ").format(
            column=sql.Identifier(PK_column),
            data_type=sql.Identifier(PK_type),
            condition=sql.Identifier(PK_condition)
        )
        query_column2 = sql.SQL("{column} {data_type} {condition}, ").format(
            column=sql.Identifier(column),
            data_type=sql.Identifier(data_type),
            condition=sql.Identifier(condition)
        )
        query_constraint = sql.SQL("FOREIGN KEY ({column}) REFERENCES {schema_PK_table}({PK_col}) );").format(
            column=sql.Identifier(PK_column),
            schema_PK_table=sql.Identifier(schema_name, PK_column),
            PK_col=sql.Identifier(PK_column)
        )
        query = sql.Composed([query_table, query_column1, query_column2, query_constraint])
        self.execute(query, "CREATE")


    def PostgreSCHEMA(self, schema_name):
        self.Create_Schema(schema_name)

    # Create Tables through Constants for database and table names
    # resources, identifiers, children, ..., schedules
    def PostgreTABLE(self, table_name="", schema_name="public", query=""):
        if query != "":
            self.execute(query, "CREATE")
        else:
            self.execute(table_name, "CREATE")
    
    def checkDataType(self, value):
        # Presume data_type 
        # dict  -> new table
        if isinstance(value, dict):
            return "dict"
        # list  -> re checkDataType
        if isinstance(value, list):
            if isinstance(value[0], str):
                data_type = "text"
            elif isinstance(value[0], int):
                data_type = "integer"
            elif isinstance(value[0], bool):
                data_type = "boolean"
            elif isinstance(value[0], float):
                data_type = "real"
            elif isinstance(value[0], dict):
                data_type = "jsonb"
            else:
                return "error"
            data_type += []
        else :
            if isinstance(value[0], str):
                data_type = "text"
            elif isinstance(value[0], int):
                data_type = "integer"
            elif isinstance(value[0], bool):
                data_type = "boolean"
            elif isinstance(value[0], float):
                data_type = "real"
            elif isinstance(value[0], dict):
                data_type = "jsonb"
            else:
                return "error"
        return data_type
                
    # PostgreDBInit.py have PK information
    def WhoPK(self, schema_name):
        if schema_name == _resources:
            return PK_resources
        elif schema_name == _identifiers:
            return PK_identifiers
        elif schema_name == _srn:
            return PK_srn
        elif schema_name == _children:
            return PK_children
        elif schema_name == _subscriptions:
            return PK_subscriptions
        elif schema_name == _statistics:
            return PK_statistics
        elif schema_name == _actions:
            return PK_actions
        elif schema_name == _batchNotifications:
            return PK_batchNotifications
        elif schema_name == _requests:
            return PK_requests
        elif schema_name == _schedules:
            return PK_schedules
        else:
            try:
                raise Exception("Schema_name or table_name is incorrect!")  
            except Exception as e:   
                print(e)
            return "error"
        
    def hasTable(self, schema_name, table_name):
        query=sql.SQL("SELECT EXISTS ( SELECT 1 FROM {} WHERE table_schema = {schema} AND table_name = {table} );").format(
            sql.Identifier("information_schema", "tables"),
            schema=sql.Literal(schema_name),
            table=sql.Literal(table_name)
        )
        result = self.execute(query=query, msg="SELECT")
        # result's type is list, [(True,)]
        if True in result[0]:
            return True
        return False
        
    def hasValue(self, schema_name, table_name, PK_col, PK_value):
        query= sql.SQL("SELECT EXISTS ( SELECT 1 FROM {schema_table} WHERE {PK} = {value});").format(
            schema_table=sql.Identifier(schema_name, table_name),
            PK=sql.Identifier(PK_col),
            value=sql.Literal(PK_value)
        )
        result = self.execute(query=query, msg="SELECT")
        # result's type is list, [(True,)]
        if True in result[0]:
            return True
        return False

    def Create_Table_Jsonb(self, data:dict):
        self.schema_name:list = data.keys() 
        PK_info:dict = data.get(self.schema_name[0])
        PK_info_key = PK_info.keys()
        PK = self.WhoPK(self.schema_name[0])

        json_data: dict = PK_info.get(PK_info_key)
        #val = [PK_info_key, [Jsonb(self.json_data)]] 
        self.insert(self, table_name = self.schema_name[0], values= [PK_info_key, Jsonb(self.json_data)], columns="", schema_name="public")
        #self.insert(self, table_name = self.schema_name[0], values= val, columns="", schema_name="public")

    def settingParm(PK, PK_value, column_name, column_value):
        if column_name == PK:
            columns = [PK]
            values = [PK_value]
        else :
            columns = [PK, column_name]
            values = [PK_value, column_value]
        return columns, values

    def Chain_Create_Table(self, schema_name, PK_value, table_info:dict, PK, PK_type, PK_condition):
        # Create_All_Table -> Chain_Create_Table(schema_name, column_value)
        # Chain_Create_Table(schema_name, sub_table_info) -> Chain_Create_Table(schema_name)
        for table_name, column_value in table_info.items():
                # column name equals table name
                column_name = table_name
                # Search and upsert ...
                if self.hasTable(schema_name, table_name):
                    if self.hasValue(schema_name, table_name):
                        self.update(schema_name, table_name, column_name, column_value, PK, PK_value)
                    else:
                        columns, values = self.settingParm(PK, PK_value, column_name, column_value)
                        self.insert(schema_name, table_name, columns, values)
                # Table is not exists
                else :
                    data_type = self.checkDataType(column_value)
                    if data_type == "error":
                        print(Exception("I don't know value's data type!!!"))
                    
                    condition = ""
                    if data_type == "dict":
                        condition = "PRIMARY KEY"
                        self.Create_Table(schema_name, table_name, PK, PK_type, PK_condition, column_name, data_type, condition)
                        #column_value:dict
                        # 그림은 여기서부터 시작한다고 생각
                        # 관점 바꿔서 생각해
                        sub_PK_values = column_value.keys()
                        for sub_PK_val in sub_PK_values:
                            columns, values = self.settingParm(PK, PK_value, column_name, column_value)
                            self.insert(schema_name, table_name, columns, values)

                            sub_table_info:dict = column_value.get(sub_PK_val)
                            self.Chain_Create_Table(schema_name, column_value)
                    else :
                    # Create table and insert data ... 
                        self.Create_Table(schema_name, table_name, PK, PK_type, PK_condition, column_name, data_type, condition)
                        columns, values = self.settingParm(PK, PK_value, column_name, column_value)
                        self.insert(schema_name, table_name, columns, values)

    # createResource()
    # 테이블이랑 컬럼 생성
    def Create_All_Table(self, data:dict):
        # schema
        # keys() return data type is list
        schema_name:list = data.keys()
        schema_name:str = schema_name[0]
        update_data:dict = data.get(schema_name)
        PK_values:list = update_data.keys()
        
        PK, PK_type, PK_condition = self.WhoPK(schema_name)
        if PK == "error":
            return Exception("Schema name is incorrect")

        for PK_val in PK_values:
            # table_info is dict
            table_info:dict = update_data.get(PK_val)
            self.Chain_Create_Table(schema_name, PK_val, table_info, PK, PK_type, PK_condition)
            
        
    # createResource()
    # 이미 생성된 테이블에 추가하는 방식
    def Add_Columns(self, table_name, columns:list, types:list, condition:list, schema_name="public"):
        assert table_name is not None, "table_name is not allowed None"
        assert columns is not None, "columns is not allowed None"
        assert condition is not None, "condition is not allowed None"
        
        for col, type, con in zip(columns, types, condition):
            query = f'ALTER TABLE {table_name} ADD COLUMN {col} {type} {con}'
            self.execute(query, 'ALTER')

        self.conn.commit()
    
    

data_resources = '''{
    "id-in": {
      "ri": "id-in",
      "rn": "cse-in",
      "csi": "/id-in",
      "rr": true,
      "csz": ["application/json", "application/cbor"],
      "acpi": ["/id-in/acpCreateACPs"],
      "poa": ["http://218.38.137.28:8080"],
      "__imported__": true,
      "pi": "",
      "ct": "20231122T011856,903926",
      "lt": "20231122T011856,903926",
      "ty": 5,
      "__rtype__": "m2m:cb",
      "__announcedTo__": [],
      "srt": [
        1,
        2,
        3,
        4,
        5,
        9,
        10,
        13,
        14,
        15,
        16,
        17,
        18,
        23,
        24,
        28,
        29,
        30,
        48,
        58,
        60,
        65,
        66,
        10001,
        10002,
        10003,
        10004,
        10009,
        10010,
        10013,
        10014,
        10016,
        10018,
        10024,
        10028,
        10029,
        10030,
        10060,
        10065,
        10066
      ],
      "srv": ["2a", "3", "4", "5"],
      "cst": 1,
      "__srn__": "cse-in",
      "__originator__": "CAdmin"
    }
}'''

thedictionary = {'price money': '$1', 'name': 'Google', 'color': '', 'imgurl': 'http://www.google.com/images/nav_logo225.png', 'charateristics': 'No Description', 'store': 'google'}

#("INSERT INTO product(store_id, url, price, charecteristics, color, dimensions) VALUES (%d, %s, %s, %d, %s, %s)", (1,  'http://www.google.com', '$20', thedictionary, 'red', '8.5x11'))
db = PostgreDBBinding(dbname='all_create')

sch = "resources"
tab = "ri"
val = "5678"
Pri = "ri"
Pri_val = "1234"
res = db.hasTable(sch, tab)
print("hasTable:", res)
res = db.hasValue(sch, tab, Pri, Pri_val)
print("hasValue:", res)
#res = db.update(sch, tab, tab, val, Pri, Pri_val)
#print("update:", res)
res = db.upsert(sch, tab, )
#try:
#    db.insert(table_name= "srn", columns= ['srn', 'ri'], values=['5678', '43'])
#    '''db.cur.execute("INSERT INTO public.resources(ri, m2m_attr) VALUES (%s, %s);", ("19011598", data_resources))
#    db.conn.commit()'''
#except Exception as e:
#    print(e)

db.__del__

