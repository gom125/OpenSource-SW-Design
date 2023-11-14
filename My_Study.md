공부를 위해 참조한 웹 사이트 모음
======================
참조: 웹사이트 devkuma, "PostgreSQL | 스키마(Schema) | 데이터베이스, 스키마, 테이블의 관계"<br>
URL: https://www.devkuma.com/docs/postgresql/데이터베이스-스키마-테이블의-관계/<br>

참조:  곰탱푸닷컴, "psycopg2로 PostgreSQL CRUD 클래스 구현하기"<br>
URL:  https://www.bearpooh.com/148<br>

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


참조: 웹사이트 devkuma, "PostgreSQL | 스키마(Schema) | 데이터베이스, 스키마, 테이블의 관계"<br>
URL: https://www.devkuma.com/docs/postgresql/데이터베이스-스키마-테이블의-관계/
