공부를 위해 참조한 웹 사이트 모음
======================
참조: 웹사이트 devkuma, "PostgreSQL | 스키마(Schema) | 데이터베이스, 스키마, 테이블의 관계"<br>
URL: https://www.devkuma.com/docs/postgresql/데이터베이스-스키마-테이블의-관계/<br>

참조: 곰탱푸닷컴, "psycopg2로 PostgreSQL CRUD 클래스 구현하기"<br>
URL:  https://www.bearpooh.com/148<br>

참조: 개인블로그, "[PostgreSQL] 데이터베이스 & 스키마 & 테이블 생성법"<br>
URL:  https://velog.io/@dailylifecoding/postgresql-create-schema-and-table#%F0%9F%A5%9D-schema-%EC%83%9D%EC%84%B1--%EC%A0%81%EC%9A%A9<br>

참조: PostgreSQL Documatation, "Chapter 8. Data Types"<br>
URL:  https://www.postgresql.org/docs/current/dataty"pe.html<br>

참조: stackoverflow, "Is postgres caching my query?"<br>
URL:  https://stackoverflow.com/questions/45155221/is-postgres-caching-my-query<br>

참조: tinyDB documantation<br>
URL:  https://tinydb.readthedocs.io/en/latest/usage.html#handling-data<br>

참조: stackoverflow, "Lock a table with ACCESS EXCLUSIVE using psycopg2?"<br>
URL: https://stackoverflow.com/questions/50325195/lock-a-table-with-access-exclusive-using-psycopg2<br>

참조: postgreSQL, "jsonb 자료형 다루기"<br>
URL: https://postgresql.kr/blog/postgresql_jsonb.html<br>

참조: 개인블로그, [DB] Postgresql Lock 파헤치기<br>
URL: https://chrisjune-13837.medium.com/db-postgresql-lock-%ED%8C%8C%ED%97%A4%EC%B9%98%EA%B8%B0-57d37ebe057<br>

2023.11.23
======================

## Storage.py 업데이트
acme 자체가 업데이트 되어 있음<br>
Storage.py가 업데이트 되어 있고 주석이 달린 것으로 보아 <br>
업데이트 실행

## 동기화를 위한 테이블 Lock 문제
결론: 쿼리로 처리한다.<br>
참조: https://stackoverflow.com/questions/50325195/lock-a-table-with-access-exclusive-using-psycopg2 <br>

각 테이블들이 업데이트와 같은 수정을 하고자 할 때 Lock을 걸고 수행을 한다.<br>
테이블에 Lock을 걸어야 하나. psycopg2에서는 connect 함수를 통해 Database에 접근한다.<br>

## Lock 처리를 위한 과정
참조: https://chrisjune-13837.medium.com/db-postgresql-lock-%ED%8C%8C%ED%97%A4%EC%B9%98%EA%B8%B0-57d37ebe057<br>
종류: Read Lock, Write Lock, Race Condition, 명시적 Lock <br>

### Read Lock - AcessShareLock
사용 예시: <b>begin;<b> select * from item;<br>
설명: begin;으로 실행하게 되면 쿼리문이 transcation으로 묶이게 되어<br>
commit이나 rollback을 입력하기 전까지 모든 쿼리문을 무시한다.<br>
Postgresql에서는 pg_catalog라는 스키마에 다양한 메타정보를 관리한다.<br>
그 중 pg_locks view는 database server에 현재 transaction에서 잡혀있는 lock에 대한 정보를 제공한다..<br>

### Write Lock - RowExclusiveLock
사용 예시: update 등등 수정을 요청하는 쿼리 발생시 자동 설정<br> 
설명: 데이터의 정합성과 무결성을 정하는 격리수준인 Isolation level이<br>
대부분의 Database에서는 Read Committed로 되어있다.<br>
이는 Commit을 한 정보만 다른 세션 또는 트렌젝션에서 확인할 수 있다는 의미다.<br>

### Racecondition - ShareLock
사용 예시: 쓰기 도중에 update와 같은 수정을 요청하는 쿼리 발생시 자동 설정<br>
설명: ShareLock은 동시 데이터를 변경할 때 생기는 문제를 보호하기 위하여<br>
먼저 Lock을 잡은 Transactionid에 공유를 요청하는 Lock이다<br>

### Explicit Lock (명시적 락)
#### Table Lock - AccessExclusiveLock
사용 예시: <b>BEGIN; Lock<b> table item <b>in ACCESS EXCLUSIVE MODE<b>; <br>
설명: 테이블 락<br>

#### RowLock — RowShareLock
사용 예시:  <b>BEGIN; SELECT<b> * FROM item WHERE id=1 <b>FOR UPDATE;<b> <br>
설명: SELECT FOR UPDATE 문은 Select 명령문 마지막에 붙여서 쓰는 명령어입니다.<br>
Select의 조회결과에 RowShareLock 을 걸어서 쓰기잠금(ExclusiveLock)을<br>
걸지 못하도록 하여 해당 row에 데이터를 변경하는 것<br>

## 데이터 일치화 문제
## postgreSQL DB 생성 문제
두 가지 같은 선상에 있는 문제다<br>
현재로서는 postgreSQL DB의 테이블을 생성하기 위한 쿼리가 존재한다.<br>
1차적으로는 해당 쿼리문을 모두 작성한 다음, <br>
쿼리문을 함수로 자동 작성하도록 만든다.<br>
2차적으로는 list가 아닌 dictionary로 쿼리문을 구성하도록 한다.<br>
3차적으로는 columns를 추가할 수 있는 쿼리를 처리하는 함수를 자동 작성하도록 구현한다.<br><br>

이후 각 테이블에 존재하는 특이한 자료형들을 처리해야 한다. <br>
any 자료형에 경우 columns를 추가할 수 있는 함수로 작성한다. <br>
struct의 경우 논의와 분석이 필요하다.<br>

현재로서 참고할만한 자료는 다음과 같다. <br>
![image](https://github.com/gom125/OpenSource-SW-Design/assets/142817235/6ec14520-e05c-495e-8e14-8b4825c32a27) <br>
참조: https://postgresql.kr/blog/postgresql_jsonb.html<br>

## Schema 생성 문제
순서<br>
1. table 생성<br>
2. schema 생성<br>
3. schema 소속 변경<br>




2023.11.21
======================

## Storage.py 분석
tinyDB를 사용할 때 cache_size라는 변수를 지정하는 데<br>
이 변수는 캐시 쿼리를 하기 위해서 사용된다. <br>

PostgreSQL에 연결할 때 cache_size를 사용하지 않거나 어떤 설정을 해야함 <br>

## TinyDB의 데이터와 Postgre의 데이터 자료형 일치화 필요
TinyDB의 데이터는 딕셔너리 형태로 저장이 되고 있다.<br>
Postgre의 데이터 자료를 일치시면 테이블의 columns로 구현이 가능하다.<br>

## Table를 생성하면서 columns을 선언하는 함수 구현 필요
columns를 작성할 때, 괄호()로 묶은 다음, 이름, 자료형, 특징을<br>
작성하는데 이를 구분할 간단한 코드와 자료형, 특징값의 공부 필요

PK는 Primary Key를 의미한다.

2023.11.14
======================

## conn 함수, Database 연결
PostgreSQL에 연결하기 위한 라이브러리, psycopg2 <br>

해당 라이브러리에서 제공하는, 아주 기초적인, 함수는 conn 함수이다.<br>
postgreSQL을 열어놓은 서버에 있는 database에 연결하는 함수이다. <br>

postgreSQL을 설치하면, psql이라는 앱도 같이 설치가 된다. <br>
psql로 postgreSQL DB를 컨트롤할 수 있다.<br>
GUI를 제공하는 pgAdmin 4를 설치해 사용할 수도 있다.<br>

초기 설치를 한 경우:<br>
"postgres"<br>
"template1"<br>
"template2"<br>
을 확인할 수 있다. (psql에서 \l 입력) <br>

conn 함수에 필요로 하는 파라미터는 다음과 같다. <br>
<b>host, dbname, user, password, port<b> <br>
host: postgreSQL DB를 열어놓은 서버의 ip 주소<br>
dbname: 연결하고자 하는 DATABASE 이름<br>
user: postgreSQL에 등록해놓은 계정, 초기 설정은 postgres(Master ID) <br>
passwd: user의 비밀번호, 초기 설정은 postgres의 비밀번호(Master PW) <br>
port: PostgreSQL DB를 열어놓은 서버의 port 번호 <br>

## postgreSQL configuration 파일
postgreSQL의 설정 정보를 담은 파일이다. <br>
저장 공간을 따로 지정하지 않은 경우, 'c:/Program Files/PostgreSQL/16/data/postgresql.conf'<br>

세부 설정 정보는 다음에 알아보기로.

## TABLE 생성후 psql과 pgAdmin에서 확인하는 법
### psql
\l <br>
![image](https://github.com/gom125/OpenSource-SW-Design/assets/142817235/b8fe29d0-209e-4499-b916-89459c36443d)
\c (db_name) <br>
\dt <br>
![image](https://github.com/gom125/OpenSource-SW-Design/assets/142817235/b7a29281-a1f6-4c52-8577-ac2f324a7907) <br>
SELECT * FROM (table_name); <br>
![image](https://github.com/gom125/OpenSource-SW-Design/assets/142817235/37360751-9a74-4d06-bccf-e3b08fda32e6)<br>

### pgAdmin
Database > Schema > Table > (생성한 table) > (Columns) <br>
![image](https://github.com/gom125/OpenSource-SW-Design/assets/142817235/7e96af42-dc03-421a-98f0-0c07ef1a4d14)<br>

## 발견한 문제점 및 주의 사항
생성하고자 하는 것이 존재하면 멈추게 됨.<br>
당연한 이야기이지만, 기존에 존재했던 목록들을 <br>
파이썬으로 반환받아 체크한 다음에 <br>
생성을 시켜야 함.<br>

\ 문자를 execute 함수에 사용했을 경우<br>
동작하지 않음

## 결론
### <b><i>기본적인 쿼리문 작동을 확인함, DBBinding 이후 제대로된 클래스와 함수 생성 필요<i><b>

2023.11.11
======================

PostgreSQL에는
1. 데이터베이스(Database)
2. 역할(사용자, Role)
3. 스키마(Schema)
가 존재한다.

PostgreSQL에는 "스키마(schema)"가 존재함.

--------------------------------------------

# PostgreSQL의 데이터 베이스, 스키마, 테이블의 관게

## 테이블
실제 데이터는 테이블에 저장이 된다.<br>
스키마가 다르면 같은 테이블 이름의 테이블도 만들 수 있음<br>
스키마마다 테이블 등의 오브젝트를 작성할 수 있는 권한을 설정할 수 있음<br>

CREATE TABLE 명령으로 테이블을 만들 경우,<br>
테이블 이름에 스키마를 생략하면 기본적으로 public 스키마에 테이블이 만들어짐.<br>
역할 이름과 같은 스키마가 생성 된 경우는 제외<br>

## 데이터베이스
테이블은 목적에 따라 여러 개 만들 수 있고 그것을 정리한 것이 데이터 베이스<br>

초기에는 템플릿 데이터베이스인 template0와 template1 그리고 postgres라는 데이터베이스가 생성됨<br>
데이터베이스는 작성 권한이 있으면 신규로 추가 할 수 있음

## 스키마(Schema)
스키마는 데이터베이스에 작성되는 테이블이나 함수 등의 개체를 그룹화하는 것<br>
스키마가 다르면 동일한 데이터베이스에도 동일한 테이블 이름으로 테이블을 만들 수 있음<br>
데이터베이스를 작성하면 자동으로 public이라는 특별한 스키마가 작성됨.<br>

public 스키마는 기본적으로 모든 역할에 권한과 Create 권한이 부여되며, <br>
public 스키마에 어떤 역할도 테이블을 만들 수 있음<br>

public 스키마와 별도로 스키마를 데이터베이스에 만들 수 있음.<br>
다른 데이터베이스 시스템에서는 사용자 이름과 동일한 이름의 스키마 이름을<br> 
가진 스키마만 작성할 수 없는 것도 있다.<br>

PosgreSQL에서는 모든 이름의 스키마를 만들 수 있음<br>


----------------------
개인적으로 비유한다면, <br>
스키마는 계정,<br>
데이터베이스는 디렉터리,<br>
테이블은 파일.<br>

스키마가 다르면 돌일한 테이블 이름으로 테이블을 만들 수 있음<br>
= 계정을 다르게 생성한 파일<br>
A 계정의 apple 파일을 지웠다고 B 계정에 apple이 지워지지는 않음

<br>
작성자: Shin_Jaehyeon


참조: 웹사이트 devkuma, "PostgreSQL | 스키마(Schema) | 데이터베이스, 스키마, 테이블의 관계"<br>
URL: https://www.devkuma.com/docs/postgresql/데이터베이스-스키마-테이블의-관계/
