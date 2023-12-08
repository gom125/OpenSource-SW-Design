
import psycopg
from psycopg.pq import Escaping
from psycopg.types.json import Jsonb
from psycopg import sql

#import datetime
import json
import os
from psycopg.pq import Escaping

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
		# json 파일 for PostgreSQL
		'fileResources',
		'fileIdentifiers',
		'fileSubscriptions',
		'fileBatchNotifications',
		'fileStatistics',
		'fileActions',
		'fileRequests',
		'fileSchedules',
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
        print()
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
            print()
            self.execute(query, "UPDATE")

    # upsert
    def upsert(self, schema_name, table_name, column, value, update_value, PK):
        query = sql.SQL("INSERT INTO {schema_table} ({column}) VALUES ({value}) ON CONFLICT ({pk}) DO UPDATE SET {column}={new_val};").format(
                schema_table=sql.Identifier(schema_name, table_name),
                column=sql.Identifier(column),
                value=sql.Literal(value),
                new_val=sql.Literal(update_value),
                pk=sql.Identifier(PK),
        )

        print(query.as_string(self.conn))
        self.execute(query=query, msg="UPSERT")
    
    def delete(self, schema_name, table_name, column, value):
        query = sql.SQL("DELETE FROM {schema}.{table} WHERE {column}={value};").format(
                schema=sql.Identifier(schema_name),
                column=sql.Identifier(column),
                table=sql.Identifier(table_name),
                value=sql.Literal(value),
        )
        print(query.as_string(self.conn))
        self.execute(query=query, msg="DELETE")

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
        query_column1 = sql.SQL("{column} {data_type} {constraint}, ").format(
            column=sql.Identifier(PK_column),
            data_type=sql.SQL(PK_type),
            constraint=sql.SQL(PK_condition) if condition else sql.SQL("")
        )
        query_column2 = sql.SQL("{column} {data_type} {constraint}, ").format(
            column=sql.Identifier(column),
            data_type=sql.SQL(data_type),
            constraint=sql.SQL(condition) if condition else sql.SQL("")
        )
        query_constraint = sql.SQL("FOREIGN KEY ({column}) REFERENCES {schema_PK_table}({PK_col}) );").format(
            column=sql.Identifier(PK_column),
            schema_PK_table=sql.Identifier(schema_name, PK_column),
            PK_col=sql.Identifier(PK_column)
        )
        query = sql.Composed([query_table, query_column1, query_column2, query_constraint])
        print(query.as_string(self.conn))
        print()
        self.execute(query, "CREATE")

    # 이미 생성된 테이블에 추가하는 방식
    def Add_Columns(self, schema_name, table_name, column_name, data_type, condition):        
        query = sql.SQL("ALTER TABLE {schema_table} ADD COLUMN {col} {type} {con}").format(
            schema_table=sql.Identifier(schema_name, table_name),
            col=sql.Identifier(column_name),
            type=sql.SQL(data_type),
            con=sql.SQL(condition)
        )
        print(query.as_string(self.conn))
        self.execute(query, 'ALTER')

    def Add_FK(self, schema_name, table_name, PK_column, column):
        query = sql.SQL("ALTER TABLE {schema_table} ADD CONSTRAINT {cons_name} FOREIGN KEY({column}) REFERENCES {schema_PK_table}({PK_column});").format(
            schema_table=sql.Identifier(schema_name, table_name),
            cons_name=sql.SQL(f'fk_{column}_{PK_column}'),
            column=sql.SQL(PK_column),
            schema_PK_table=sql.Identifier(schema_name, PK_column),
            PK_column=sql.SQL(PK_column)
        )
        print(query.as_string(self.conn))
        self.execute(query, "ALTER")

    def Add_PK(self, schema_name, table_name, column):
        query = sql.SQL("ALTER TABLE {schema_table} ADD PRIMARY KEY ({column});").format(
            schema_table=sql.Identifier(schema_name, table_name),
            column=sql.SQL(column)
        )
        print(query.as_string(self.conn))
        self.execute(query, "ALTER")

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
        print("checkDataType(value):", type(value), value)
        if isinstance(value, dict):
            return "dict"
        if value == None:
            return "error"
        # list  -> re checkDataType
        if isinstance(value, list):
            if len(value) == 0 :
                return "text[]"
            if isinstance(value[0], str):
                data_type = "text"
            elif isinstance(value[0], bool):
                data_type = "boolean"
            elif isinstance(value[0], int):
                data_type = "integer"
            elif isinstance(value[0], float):
                data_type = "real"
            elif isinstance(value[0], dict):
                return "jsonb"
            else:
                return "error"
            data_type += "[]"
        else :
            if isinstance(value, str):
                data_type = "text"
            elif isinstance(value, bool):
                data_type = "boolean"
            elif isinstance(value, int):
                data_type = "integer"
            elif isinstance(value, float):
                data_type = "real"
            elif isinstance(value, dict):
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
    
    def hasColumn(self, schema_name, table_name, column1, column2):
        query=sql.SQL("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = {schema} AND TABLE_NAME = {table} AND COLUMN_NAME IN ( {col1}, {col2} )").format(
            schema=sql.Literal(schema_name),
            table=sql.Literal(table_name),
            col1=sql.Literal(column1),
            col2=sql.Literal(column2)
        )
        print(query.as_string(self.conn))
        res = self.execute(query, "SELECT")
        #print(type(res), len(res), res)
        if len(res) == 2:
            return True
        return False
        
    def hasValue(self, schema_name, table_name, column_name1, column_value1, column_name2="", column_value2=""):
        # PK search
        query= sql.SQL("SELECT EXISTS ( SELECT 1 FROM {schema_table} WHERE {column} = {value}").format(
            schema_table=sql.Identifier(schema_name, table_name),
            column=sql.Identifier(column_name1),
            value=sql.Literal(column_value1)
        )
        # attr search
        if column_name2 != "" and column_value2 != "":
            query2= sql.SQL(" AND {column} = {value});").format(
                column=sql.Identifier(column_name2),
                value=sql.Literal(column_value2)
            )
        else:
            query2= sql.SQL(");")
        
        result = self.execute(query=sql.Composed([query, query2]), msg="SELECT")
        # result's type is list, [(True,)]
        if True in result[0]:
            return True
        return False

    def settingParm(self, PK_name, PK_value, column_name, column_value):
        if column_name == PK_name:
            columns = [PK_name]
            values = [PK_value]
        else :
            columns = [PK_name, column_name]
            values = [PK_value, column_value]
        print("setting parameter:", columns, values)
        return columns, values

    def Chain_Create_Table(self, schema_name, PK_value, table_info:dict, PK_name, PK_type, PK_condition):
        # Create_All_Table -> Chain_Create_Table(schema_name, column_value)
        # Chain_Create_Table(schema_name, sub_table_info) -> Chain_Create_Table(schema_name)
        # First. PK table is already exists...
        #        query = sql.SQL("INSERT INTO {schema}.{table} ({column}) VALUES ({value}) ON CONFLICT ({pk}) DO UPDATE SET {column}={new_val};")
        self.upsert(schema_name, PK_name, PK_name, PK_value, PK_value, PK_name)
        # Second. other...
        for column_name, column_value in table_info.items():
            if column_name == PK_name:
                continue
            # column name equals table name
            table_name = column_name

            data_type = self.checkDataType(column_value)
            if data_type == "jsonb":
                column_value = Jsonb(column_value)

            condition = ""
            # dict == column_value is sub_table_info
            if data_type == "dict":
                # sub_PK_type           == data_type                == column_value's data type
                data_type = "varchar(255)"
                # sub_PK_condition      == condition                == column_value's condition == 
                condition = "PRIMARY KEY"
                # sub_PK_name           == column_name
                # sub_table_info        == column_value
                # sub_PK_values         == sub_table_info's keys    == sub_column_names == column_value's keys
                sub_PK_values = column_value.keys() # type is not list...
                # sub_PK_val            == sub_PK_value             == sub_column_name
                for sub_PK_val in sub_PK_values:
                    # sub_column_value  == sub_table_info's value   == sub_column_value == column_value's value
                    sub_column_value = column_value.get(sub_PK_val)

                    if self.hasTable(schema_name, table_name):
                        # Exist
                        # Does the value exist?
                        addColumn = self.hasColumn(schema_name, table_name, PK_name, column_name) 
                        if addColumn == False:
                            self.Add_Columns(schema_name, table_name, PK_name, PK_type, "")

                        if self.hasValue(schema_name, table_name, PK_name, PK_value, column_name, sub_PK_val):
                            # Exist
                            # table_name---------------------
                            # "PK_name" |  "column_name"    |
                            # "PK_value"|  "sub_PK_value"   |
                            # -------------------------------
                            # update data
                            self.update(schema_name, table_name, column_name, sub_PK_val, PK_name, PK_value)
                        else:
                            # Does not Exist
                            # table_name---------------------
                            # PK_name   |   column_name     |
                            # -         |   -               |
                            # -------------------------------
                            # insert data
                            columns, values = self.settingParm(PK_name, PK_value, column_name, sub_PK_val)
                            self.insert(schema_name, table_name, columns, values)

                        if addColumn == False:
                            self.Add_FK(schema_name, table_name, PK_name, column_name)

                        # Create sub table using sub_table_info
                        # tab_id == table_name
                        # case: pv - acr, pvs - acr
                        # table_name---------------------  ->   sub_PK_value--------------------------------- 
                        # PK_name   |   column_name     |       column_name:tab_id  | sub_column_name   |
                        # PK_value  |   sub_PK_value    |          -                |   -               |
                        # -------------------------------       ---------------------------------------------
                        ### initial function ###
                        #elf.Chain_Create_Table(schema_name, PK_value  , table_info    , PK_name    , PK_type  , PK_condition)
                        ### recursive function ###
                        #elf.Chain_Create_Table(schema_name, sub_PK_val, sub_table_info, sub_PK_name, data_type, condition)
                        self.Chain_Create_Table(schema_name, sub_PK_val, column_value, column_name, data_type, condition)
                    else:
                        # Create Table
                        # table_name---------------------
                        # PK_name   |   column_name     |
                        # -         |   -               |
                        # -------------------------------
                        self.Create_Table(schema_name, table_name, PK_name, PK_type, "", column_name, data_type, condition)
                        
                        # Insert Value
                        # table_name---------------------
                        # PK_name   |   column_name     |
                        # PK_value  |   sub_PK_value    |
                        # -------------------------------
                        columns, values = self.settingParm(PK_name, PK_value, column_name, sub_PK_val)
                        self.insert(schema_name, table_name, columns, values)

                        # Create sub table using sub_table_info
                        ### initial function ###
                        #elf.Chain_Create_Table(schema_name, PK_value  , table_info    , PK_name    , PK_type  , PK_condition)
                        ### recursive function ###
                        #elf.Chain_Create_Table(schema_name, sub_PK_val, sub_table_info, sub_PK_name, data_type, condition) 
                        self.Chain_Create_Table(schema_name, sub_PK_val, column_value, column_name, data_type, condition)

            # not dict == search -> (update) or (create -> insert)
            else:
                # Does the table exist?
                if self.hasTable(schema_name, table_name):
                    # Exist
                    addColumn = self.hasColumn(schema_name, table_name, PK_name, column_name) 
                    if addColumn == False:
                        self.Add_Columns(schema_name, table_name, PK_name, PK_type, "")
                    # Does the value exist?
                    if self.hasValue(schema_name, table_name, PK_name, PK_value, column_name, column_value):
                        # Exist
                        # table_name---------------------
                        # "PK_name" |  "column_name"    |
                        # "PK_value"|  "column_value"   |
                        # -------------------------------
                        self.update(schema_name, table_name, column_name, column_name, PK_name, PK_value)
                    else:
                        # Does not Exist
                        # table_name---------------------
                        # PK_name   |   column_name     |
                        # -         |   -               |
                        # -------------------------------
                            
                        columns, values = self.settingParm(PK_name, PK_value, column_name, column_value)    
                        self.insert(schema_name, table_name, columns, values)
                    
                    if addColumn == False:
                        self.Add_FK(schema_name, table_name, PK_name, column_name)
                    
                else:   
                    # Does not exist 
                    # Create Table
                    self.Create_Table(schema_name, table_name, PK_name, PK_type, PK_condition, column_name, data_type, condition)
                    # Insert value
                    columns, values = self.settingParm(PK_name, PK_value, column_name, column_value)
                        
                    self.insert(schema_name, table_name, columns, values)  

    # createResource()
    # 테이블이랑 컬럼 생성
    def Create_All_Table(self, data:dict):
        # schema
        # keys() return data type is list
        schema_name:list = list(data.keys())
        schema_name:str = schema_name[0]
        update_data:dict = data.get(schema_name)
        PK_values:list = list(update_data.keys())
        
        PK, PK_type, PK_condition = self.WhoPK(schema_name)
        if PK == "error":
            return Exception("Schema name is incorrect")

        for PK_val in PK_values:
            # table_info is dict
            table_info:dict = update_data.get(PK_val)
            self.Chain_Create_Table(schema_name, PK_val, table_info, PK, PK_type, PK_condition)

    def Create_Table_Jsonb(self, data:dict):
        self.schema_name:list = list(data.keys()) 
        PK_info:dict = data.get(self.schema_name[0])
        PK_info_key = list(PK_info.keys())
        PK = self.WhoPK(self.schema_name[0])

        json_data: dict = PK_info.get(PK_info_key)
        #val = [PK_info_key, [Jsonb(self.json_data)]] 
        self.insert(self, table_name = self.schema_name[0], values= [PK_info_key, Jsonb(self.json_data)], columns="", schema_name="public")
        #self.insert(self, table_name = self.schema_name[0], values= val, columns="", schema_name="public")
     
    
current_directory = os.path.dirname(__file__)
json_file_path = os.path.join(current_directory, 'resource.json')

with open(json_file_path, "r") as f:
    data_resources = json.load(f) 



print("===============================")
#("INSERT INTO product(store_id, url, price, charecteristics, color, dimensions) VALUES (%d, %s, %s, %d, %s, %s)", (1,  'http://www.google.com', '$20', thedictionary, 'red', '8.5x11'))

db = PostgreDBBinding(dbname='test_v2')
#db.hasColumn("resources", "acr", "acr", "pvs")
#db.Add_Columns("resources", "acr", "pvs", "varchar(255)", "")
#db.Add_FK("resources","acr", "pvs", "pvs")
db.Create_All_Table(data_resources)
db.__del__

#sch = "resources"
#tab = "ri"
#val = "5678"
#Pri = "ri"
#Pri_val = "1234"
#res = db.hasTable(sch, tab)
#print("hasTable:", res)
#res = db.hasValue(sch, tab, Pri, Pri_val)
#print("hasValue:", res)
#res = db.update(sch, tab, tab, val, Pri, Pri_val)
#print("update:", res)
#res = db.upsert(sch, tab, )
#try:
#    db.insert(table_name= "srn", columns= ['srn', 'ri'], values=['5678', '43'])
#    '''db.cur.execute("INSERT INTO public.resources(ri, m2m_attr) VALUES (%s, %s);", ("19011598", data_resources))
#    db.conn.commit()'''
#except Exception as e:
#    print(e)

#db.__del__

