import psycopg2

# Connect to your postgres DB
# conn = psycopg2.connect("host=localhost dbname=PostgreSQL16_ACME user=postgres password=post1234")

class PostgreDB():
    # Connect PostgresDB 
    def __init__(self, host, dbname, user, password, port):
        self.host = 'localhost'
        self.dbaname = 'postgres'
        self.user = 'postgres'
        self.password = 'post124'
        self.port = 8080
    
        try:
            self.conn = psycopg2.connect(host=self.host, dbname=self.dbaname, user=self.user, password=self.password, port=self.port)

        except Exception as e:
            print(e)
        else:
            self.cur = self.conn.cursor()

    # 종료
    def __del__(self):
        self.cur.close()
        self.conn.close()

    # Execute
    def execute(self, query, msg=""):
        assert query is not None, "query is not allowed None"
        assert msg is not None, "msg is not allowed None"

        try:
            self.cur.execute(query)

            is_select = query.upper().startswitch('SELECT ')
            result = None

            if is_select:
                result = self.cur.fetchall()
            else:
                self.conn.commit()
            
            return result
        except Exception as e:
            print("Error Occured in {msg} Data!", format(msg=msg), e)
    
    # 테이블 이름 생성
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

        insert_sql = "INSERT INTO {schema_table} ({column}) VALUES ('{data}');".foramt(schema_table=schema_table, column=column_name, data=data)
        
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
    

db = PostgreDB()

