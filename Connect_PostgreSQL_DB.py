import psycopg2
from Storage import *

#####################################################
#   Goal: Create and Control PostgreSQL DB
#   Problem Example: Create Student Database
#  
#   School Database
#       Student Table:
#           1. Student ID
#           2. Name
#           3. Age
#           4. Grade
#   
#       Class Table:
#           1. Class ID
#           2. Name
#           3. Teacher
#           4. Class Time
#
#   Update Student ID
#   Delete Class Time
#   Retrieve Student ID
#   
#   



class PostgreDB():
    __slots__ = (
        # For Connect PostgreSQL DB Server
        'host', 
        'dbname', 
        'user', 
        'password',
        'port',
        'autocreate',
        'autocommit',
        # Connect and Control
        'conn',
        'cur',
        # Create
        'schema_name',
        'table_name',
		# acme와 연결하기 위한 경로 및 초기 설정
		'path',
		'cacheSize',    # 쿼리 캐시
		'writeDelay',
		'maxRequests',
		# 동기화 문제를 위한 초기 설정
		'lockResources',
		'lockIdentifiers',
		'lockChildResources',
		'lockStructuredIDs',
		'lockSubscriptions',
		'lockBatchNotifications',
		'lockStatistics',
		'lockActions',
		'lockRequests',
		# json 파일 for PostgreSQL
		'fileResources',
		'fileIdentifiers',
		'fileSubscriptions',
		'fileBatchNotifications',
		'fileStatistics',
		'fileActions',
		'fileRequests',
		# ACME 리소스
		'dbResources',
		'dbIdentifiers', 		
		'dbSubscriptions', 	
		'dbBatchNotifications',
		'dbStatistics',
		'dbActions',	
		'dbRequests',	
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
	)

    # Connect PostgresDB 
    def __init__(self, host='localhost', dbname='postgres', user='postgres', password='post1234', port=5432, autocreate=False):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.autocreate = autocreate  # Auto-create 'DBname' Database
    
        try:
            self.conn = psycopg2.connect(host=self.host, dbname=self.dbname, user=self.user, password=self.password, port=self.port)
            
        except Exception as e:
            print(e)
            
            if self.autocreate:
                # DATABASE 자동 생성
                # 마스터 계정인 postgres로 진입 후
                # 접근하고자 하는 데이터 베이스 생성
                self.conn = psycopg2.connect(host=self.host, dbname='postgres', user=self.user, password=self.password, port=self.port)
                self.cur = self.conn.cursor()

                autocommit = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
                print("ISOLATION_LEVEL:", psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                self.conn.set_isolation_level(autocommit)
                self.Create_Database(dbname=self.dbname)            

                self.conn = psycopg2.connect(host=self.host, dbname=self.dbname, user=self.user, password=self.password, port=self.port)
        else:
            self.cur = self.conn.cursor()

        

    # 종료
    def __del__(self):
        self.cur.close()
        self.conn.close()

    # psycopg2's wrapper function (execute)
    # msg is what your initial query or purpose 
    # SELECT, UPDATE, CREATE, ...
    def execute(self, query, msg=""):
        assert query is not None, "query is not allowed None"
        assert msg is not None, "msg is not allowed None"

        try:
            self.cur.execute(query)

            is_select = query.upper().startswith('SELECT ')
            result = None

            if is_select:
                result = self.cur.fetchall()
            else:
                self.conn.commit()
            
            return result
        except Exception as e:
            print("Error Occured in {msg} Data!", format(msg=msg), e)

    # Create Database
    def Create_Database(self, dbname):
        assert dbname is not None, "dbname is not allowed None"
        query = f'CREATE DATABASE {dbname}'
        self.execute(query, 'CREATE')

    # 테이블만 생성
    def Create_Table(self, table_name, columns:list, types:list, condition:list, schema_name="public"):
        assert table_name is not None, "table_name is not allowed None"
        assert columns is not None, "columns is not allowed None"
        assert condition is not None, "condition is not allowed None"

        # 스키마가 public
        if schema_name == "public":
            query = f'CREATE TABLE {table_name} ('
            for col, type, con in zip(columns, types, condition):
                query += f'{col} {type} {con}'
                if col != columns[-1] :
                    query += ','    
            query += f');'

            print("query: ", query)
            self.execute(query, 'CREATE')
        # 스키마가 다를때, 아직 미구현
        else :
            self.schema_name = schema_name
            # schema 추가 필요
            print("Schema version not yet")

        db.conn.commit()
        

    # 이미 생성된 테이블에 추가하는 방식
    def Add_Columns(self, table_name, columns:list, types:list, condition:list, schema_name="public"):
        assert table_name is not None, "table_name is not allowed None"
        assert columns is not None, "columns is not allowed None"
        assert condition is not None, "condition is not allowed None"
        
        for col, type, con in zip(columns, types, condition):
            query = f'ALTER TABLE {table_name} ADD COLUMN {col} {type} {con}'
            self.execute(query, 'ALTER')

        db.conn.commit()
    # 테이블과 columns을 동시에 생성
    # def Create_Table_Columns

    # columns 변경
    # def Modify_Columns

    '''# 테이블 이름 생성
    def make_table_name(self, schema_name, table_name):
        assert schema_name is not None, "schema_name is not allowed None"
        assert table_name is not None, "table_name is not allowed None"

        # schema가 지정되지 않으면 table_name만 사용
        # schema의 SEARCH_PATH에 따라 테이블 탐색
        if schema_name == "":
            schema_table = table_name
        # schema가 지정되어 있으면 schema_name, table_name 형태로 생성
        else :
            schema_table = ".".join([schema_name, table_name])
        
        return schema_table

    # 레코드를 데이터베이스의 특정 테이블에 입력하는 함수
    def insert(self, table_name, column_name, data, schema_name=""):
        assert table_name is not None, "table_name is not allowed None value!"
        assert column_name is not None, "column_name is not allowed None value!"
        assert data is not None, "data is not allowed None value!"
        assert schema_name is not None, "schema_name is not allowed None value!"

        schema_table = self.make_table_name(schema_name, table_name)

        insert_sql = "INSERT INTO {schema_table} ({column}) VALUES ('{data}');".format(schema_table=schema_table, column=column_name, data=data)
        
        result = self.execute(insert_sql, "insert")

        return result
    
    # 조회
    def select(self, table_name, columns, conditions="", schema_name=""):
        assert table_name is not None, "table_name is not allowed None value!"
        assert columns is not None, "columns is not allowed None"
        assert conditions is not None, "conditions is not allowed None"
        assert schema_name is not None, "schema_name is not allowed None"

        schema_table = self.make_table_name(schema_name, table_name)

        select_sql = "SELECT {columns} FROM {schema_table};".format(columns=columns, schema_table=schema_table)

        # 검색 조건이 있으면 쿼리문 뒷 부분에 추가
        if conditions != "":
            select_sql.replace(";", " WHERE {conditions};".format(conditions = conditions))

        result = self.execute(select_sql, "Select")

        return result

    # 수정
    def update(self, table_name, column_name, value, conditions="", schema_name=""):
        assert table_name is not None, "table_name is not allowed None value!"
        assert column_name is not None, "column_name is not allowed None"
        assert value is not None, "value is not allowed None"
        assert conditions is not None, "conditions is not allowed None"
        assert schema_name is not None, "schema_name is not allowed None"

        schema_table = self.make_table_name(schema_name, table_name)

        update_sql = "UPDATE {schema_table} SET {column}='{value}';".format(schema_table=schema_table, column=column_name, value=value)

        # 검색 조건이 있으면 쿼리문 뒷 부분에 추가
        if conditions != "":
            update_sql.replace(";", " WHERE {conditions};".format(conditions = conditions))

        result = self.execute(update_sql, "Update")
       
        return result
    
    # 삭제
    def delete(self, table_name, conditions="", schema_name=""):
        assert table_name is not None, "table_name is not allowed None value!"
        assert conditions is not None, "conditions is not allowed None"
        assert schema_name is not None, "schema_name is not allowed None"

        schema_table = self.make_table_name(schema_name, table_name)

        delete_sql = "DELETE FROM {schema_table};".format(schema_table=schema_table)
        # 검색 조건이 있으면 쿼리문 뒷 부분에 추가
        if conditions != "":
            delete_sql.replace(";", " WHERE {conditions};".format(conditions = conditions))

        result = self.execute(delete_sql, "Delete") 
       
        return result
    
    # 테이블 생성
    def create_table(self, schema_name, table_name, columns):
        # columns는 [컬럼명 데이터타입 제약조건] 등으로 정의 된 문자열 형태
        # CREATE TABLE의 예제를 참고한다.

        # 전달 받은 인자가 None 값인지 확인       
        assert schema_name is not None, "schema_name is not allowed None value!"
        assert table_name is not None, "table_name is not allowed None value!"
        assert columns is not None, "columns is not allowed None"
               
        # PostgreSQL에 사용할 테이블이 존재하는지 확인
        search_sql = "SELECT pg_tables.schemaname, pg_tables.tablename FROM pg_catalog.pg_tables "
        search_sql += f"WHERE tablename='{table_name}' AND schemaname='{schema_name}';"
       
        result = None
        try:
            result = self.execute(search_sql, "Check Table")
        except Exception as e:  # 쿼리 실행에 오류가 발생한 경우
            result = ("Error Occured in Search Schema!", e)
            return result

        # 이미 테이블이 존재하는 경우 생성하지 않음
        if result:
            print("Table is already exist!")
            return result

        schema_table = self.make_table_name(schema_name, table_name)

        # 테이블 생성 진행
        create_sql = "CREATE TABLE {schema_table} ({columns});".format(schema_table=schema_table, columns=columns)       
        result = self.execute(create_sql, "Create Table")
       
        return result
    
    # 데이터 베이스 생성 함수
    # CREATE DATABASE {database_name}
    # CREATE DATABASE {database_name} TABLESPACE {tablespace_name}

    # 데이터 베이스 삭제 함수'''


testDB = "acme"
db = PostgreDB(dbname=testDB, autocreate=True)
# \ 사용 불가
#db.cur.execute('\c ' + testDB + ';')
print("DATABASE JUMP Successfully!")

table_name = 'srn'
colm = ['snr', 'ri']
ty=['VARCHAR (16)', 'VARCHAR (16)']
cond = ['PRIMARY KEY', 'NOT NULL']

db.Create_Table(table_name=table_name, columns=colm, types=ty, condition=cond)
'''db.cur.execute("""CREATE TABLE Student(
            student_id BIGSERIAL PRIMARY KEY,
            name VARCHAR (30) UNIQUE NOT NULL,
            Age SERIAL NOT NULL,
            grade CHAR (1) NOT NULL);
            """)
'''
db.conn.commit()
print("CREATE TABLE Successfully!")

db.cur.execute('SELECT * FROM Student;')
rows = db.cur.fetchall()

# Insert 쿼리 작성 후 체크
print("print Table's values")
for row in rows:
    print(f'{testDB}: {row}')

db.conn.commit()
db.__del__()
'''
db.create_table(schema_name="public", table_name="student", columns="Student_ID character[8]")
db.create_table(schema_name="public", table_name="student", columns="Student_ID character[8]")

db.insert(table_name="student", column_name="Student_ID", data="19011000", schema_name="public")
p = db.select(table_name="student", columns="Student_ID", conditions="", schema_name="public")
print(p)
'''
# ...