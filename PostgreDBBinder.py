
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
_batchNotifications = 'batchNotifications'
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

        # Create tables
        # PostgreDBInit
        self.PostgreTABLE(query=resources_query)
        self.PostgreTABLE(query=identifiers_query)
        self.PostgreTABLE(query=srn_query)
        self.PostgreTABLE(query=children_query)
        self.PostgreTABLE(query=subscriptions_query)
        self.PostgreTABLE(query=statistics_query)
        self.PostgreTABLE(query=actions_query)
        self.PostgreTABLE(query=batchNotifications_query)
        self.PostgreTABLE(query=requests_query)
        self.PostgreTABLE(query=schedules_query)
    
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


    # create
    # CREATE DATABASE {database_name}
    # CREATE TABLE {table_name}
    def create(self, query):
        self.execute(query=query, msg='CREATE')

    # insert
    # INSERT INTO {schema_name}.{table_name}({column1}, {column2}, ...) VALUES ({value1}, {value2}, ...)
    def insert(self, table_name:str, values:list, columns:list, schema_name="public"):
        query = sql.SQL("INSERT INTO {field}.{table}({column}) VALUES({value});").format(
            field=sql.Identifier(schema_name),
            table=sql.Identifier(table_name),
            column=sql.SQL(', ').join(map(sql.Identifier, columns)),
            value=sql.SQL(', ').join(map(sql.Literal, values))
            )
        print(query.as_string(self.conn))
        self.execute(query=query, msg="INSERT")
        self.conn.commit()

    # update
    def update(self, table_name, columns, values, condition, query):
        query = f"UPDATE {table_name}" 
        query += f'SET '

        pass

    # upsert
    def upsert(self, query):

        pass

    '''select: 
            SELECT {column_name} FROM {schema_name}.{table_name} WHERE {condition} order by {column_name2} desc/asc
            condition: {condition} AND {condition} OR {condition} ...
            order by desc(내림차순), asc(오름차순)으로 출력

            table:
                SELECT * FROM {schema_name}.{table_name}
            column:
                SELECT {column1}, {column2}, ... FROM {schema_name}.{table_name}
    '''

    def search(self, query):
        
        pass

    # Create Database
    def Create_Database(self, dbname):
        #autocommit = psycopg.IsolationLevel
        #print("ISOLATION_LEVEL:", psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        #self.conn.set_isolation_level(autocommit)
        #self.conn._set_autocommit
        """Setting Database option"""
        query = f'CREATE DATABASE {dbname}'
        self.execute(query, 'CREATE')
        """Create Database"""

    # Create Tables through Constants for database and table names
    # resources, identifiers, children, ..., schedules
    def PostgreTABLE(self, table_name, schema_name="public", query=""):
        if query != "":
            self.execute(query, "CREATE")
        else:
            self.execute(table_name, "CREATE")

    
    def checkDataType(self, value):
        # Presume data_type 
        if not isinstance(value, dict):
            if all(isinstance(elem, int) for elem in value):
                data_type = "INTEGER"
            elif all(isinstance(elem, bool) for elem in value):
                data_type = "BOOLEAN"
            elif all(isinstance(elem, float) for elem in value):
                data_type = "REAL"
            else:
                data_type = "text"
            if isinstance(value, list):
                data_type += "[]"
        else:
            data_type = "DICT"
        return data_type
    
    def WhoPK(self, schema_name):
        if schema_name == _resources:
            return "ri"
        elif schema_name == _identifiers:
            return "ri"
        elif schema_name == _srn:
            return "srn"
        elif schema_name == _children:
            return "ri"
        elif schema_name == _subscriptions:
            return "ri"
        elif schema_name == _statistics:
            return ""
        elif schema_name == _actions:
            return "ri"
        elif schema_name == _batchNotifications:
            return ""
        elif schema_name == _requests:
            return "ts"
        elif schema_name == _schedules:
            return "ri"
        else:
            try:
                raise Exception("Schema_name or table_name is incorrect!")  
            except Exception as e:   
                print(e)
            return "error"

    def Create_Table_Jsonb(self, data:dict):
        self.schema_name:list = data.keys() 
        PK_info:dict = data.get(self.schema_name[0])
        PK_info_key = PK_info.keys()
        PK = self.WhoPK(self.schema_name[0])

        json_data: dict = PK_info.get(PK_info_key) 
        self.insert(self, table_name = self.schema_name[0], values= [PK_info_key, Jsonb(self.json_data)], columns="", schema_name="public")
        

    # createResource()
    # 테이블이랑 컬럼 생성
    def Create_All_Table(self, data:dict):
        # schema
        # keys() return data type is list
        self.schema_name = data.keys() 
        # schema's value: dict, {PK : table}
        # PK_info is dict
        PK_info = data.get(self.schema_name[0])
        # PK_info_key is dict's key
        PK_info_key = PK_info.keys()
        PK = self.WhoPK(self.schema_name[0])
        if PK == "error":
            return Exception("Schema name is incorrect")
        
        for key in PK_info_key:
            # table_info is dict
            table_info = PK_info.get(key)
            for table_key, table_value in table_info.items():

                # search, SELECT
                # if table exist
                #   if value exist 
                #       update
                #   else
                #       insert
                # else
                #   create and insert
                pass

        query = ""

        print("query: ", query)
        self.execute(query, 'CREATE')
        self.conn.commit()
        
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
db = PostgreDBBinding(dbname='school')

try:
    db.insert(table_name= "srn", columns= ['srn', 'ri'], values=['5678', '43'])
    '''db.cur.execute("INSERT INTO public.resources(ri, m2m_attr) VALUES (%s, %s);", ("19011598", data_resources))
    db.conn.commit()'''
except Exception as e:
    print(e)
db.__del__

