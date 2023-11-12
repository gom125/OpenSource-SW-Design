## 코드 간단 설명
PostgreDB 클래스로 구현

__init__을 통해 PostgreSQL하고 연결하며, CRUD를 구현함

## 고찰

1. ACME에 연결하기 위해서
TinyDBBinding 클래스에서 사용하고 있는<br>
__slot__을 그대로 사용하여 구현해야 함.<br>

2. json 파일로 PostgreSQL을 사용하는 법 공부 필요

3. TinyDBBinding에 있는 함수들을 PostgreDB에 구현 필요

## 목표: 로컬호스트 PostgreSQL에 연결하여 CRUD 응용

schema를 공부하고 간단한 예제를 구현해 직접 테이블과 데이터베이스를 생성해 볼 것

### 예제: <br>
1. 학생 테이블
  * 학생 ID
  * 이름
  * 나이
  * 학년
2. 수업 테이블
   * 수업 ID
   * 수업명
   * 수업 교사
   * 수업 시간: 수업 시작 시간 또는 수업을 진행한 시간으로 생성

![image](https://github.com/gom125/OpenSource-SW-Design/assets/142817235/b1d69963-c10b-447a-b0e1-e27dc472bb91)

![Uploading image.png…]()

## 목표: ACEM에 연결하기 위한 TinyDBBinding 클래스 분석
TINYDB를 사용하여 선언하는 부분 분석 필요
json 파일을 통해 PostgreSQL에 바인딩하는 부분 분석 필요

## 코드 참조
참조:  곰탱푸닷컴, "psycopg2로 PostgreSQL CRUD 클래스 구현하기"
URL:  https://www.bearpooh.com/148
