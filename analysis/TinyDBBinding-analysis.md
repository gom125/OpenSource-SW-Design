# TinyDBBinding

TinyDB 테이블 구조 및 리소스 

<img width="721" alt="image" src="https://github.com/leesangwooon/ACME/assets/144790879/a1dd72aa-db28-4f5e-b220-d59e7b25aad7">

(테이블 단위의 메서드 작업은 with self.lock~ 블럭 내에서 이루어짐 -> 작업에 앞서 테이블 단위로 락을 걸어 동기화 문제 해결)

#### _assignConfig()
cacheSize, writeDelay,maxRequests 받아옴 (Configuration.py)

#### closeDB()
db의 모든 테이블 연결 해제 (TinyDB Table.close() 이용)

#### purgeDB()
db의 모든 테이블 삭제 (TinyDB Table.truncate() 이용)

#### backupDB
db의 모든 테이블의 데이터(메타데이터 포함)을 복사하여 인자로 받은 dir 경로에 저장 (pathlib 모듈 Path(), shutil 모듈 copy2() 이용)

## Resources - resources table
<img width="350" alt="image" src="https://github.com/leesangwooon/ACME/assets/144790879/16531bee-8f00-47e1-83b8-3726899d2854">

#### insertResource()
테이블에 리소스 insert (TinyDB Table.insert() 이용)

#### upsertResource()
테이블에 리소스 update or insert (TinyDB Table.upsert() 이용)

#### updateResource()
테이블에 리소스 update 및 해당 리소스 딕셔너리 내 null 데이터 삭제 (TinyDB Table.update() 이용)

#### deleteResource()
테이블에 리소스 delete (TinyDB Table.remove() 이용)

#### searchResources()
인자로 받은 데이터 기반으로 해당 데이터를 포함하는 리소스 리스트 반환 (TinyDB Table.search() 이용)

#### discoverResourcesByFilter()
필터 함수(입력: JSON, 출력:bool) 조건에 맞는 리소스 리스트 반환 (TinyDB Table.search() 이용)

#### hasResource()
인자로 전달받은 데이터를 포함하는 리소스 존재 여부 반환 (TinyDB Table.contains() 이용)

#### countResources()
리소스의 개수 반환 (파이썬 내장함수 len() 이용)

#### searchByFragment()
인자로 전달받은 딕셔너리의 리소스를 검색하여 리스트로 반환 (TinyDB Table.search() 이용)

## Identifiers - identifiers/srn/children table
<img width="346" alt="image" src="https://github.com/leesangwooon/ACME/assets/144790879/f8f15fee-3f1f-4ad1-bae7-edc1f4a20838">

#### upsertIdentifier()
identifiers 테이블에 (ri, rn, srn, ty), srn 테이블에 (srn, ri) update or insert (TinyDB Table.update() 이용)

#### deleteIdentifier()
identifiers 테이블, srn 테이블에서 인자로 받은 리소스에 대한 ri, srn 각각 삭제  (TinyDB Table.remove() 이용)

#### searchIdentifiers()
identifiers 테이블, srn 테이블에서 (ri, srn) 데이터로 리소스 검색하여 리스트로 반환 (TinyDB Table.get() 이용)

#### upsertChildResource()
children 테이블에 리소스 upsert 후 부모 리소스와 자식 리소스 연결 (TinyDB Table.upsert/get/update() 이용)

#### removeChildResource()
children 테이블에서 자식 리소스를 삭제하고 부모 리소스에서 자식 리소스 삭제(부모의 ch 리소스 업데이트) (TinyDB Table.remove/update() 이용)

#### searchChildResourcesByParentRI()
children 테이블에서 부모(pi)에 대응되는 자식 리소스를 찾아 반환 (ty로 리소스 타입 필터링) (TinyDB Table.get() 이용)

## Subscriptions - subscribtions table
<img width="349" alt="image" src="https://github.com/leesangwooon/ACME/assets/144790879/6f55124c-6f95-4437-ad7d-5e08cbabfd61">


#### searchSubscriptions()
subscription 테이블에서 ri 혹은 pi 값으로 구독 정보를 조회하여 리스트로 반환 (TinyDB Table.get/search() 이용)

#### upsertSubscription()
subscription 테이블 리소스 upsert (ri, pi, nct, net, atr, chty, exc, ln, nus, bn, cr, nec, org, ma, nse) (TinyDB Table.upsert() 이용)

#### removeSubscription()
subscription 테이블에서 해당 ri를 가진 객체 모두 삭제 후 삭제한 객체 수 반환 (TinyDB Table.remove() 이용)

## BatchNotifications - BatchNotifications table
<img width="350" alt="image" src="https://github.com/leesangwooon/ACME/assets/144790879/11c379a6-e798-4733-820f-4a08c1a0bb1c">

#### addBatchNotification()
배치 알림 추가 (TinyDB Table.insert() 이용)
- ri: resource ID
- nu: 알림 받을 대상의 uri
- tstamp: 알림 시간
- request: 알림 요청 (JSON 형식)


#### countBatchNotifications()
BatchNotifications 테이블에서 인자로 전달받은 ri와 nu 값이 모두 일치하는 객체의 수를 count (TinyDB Table.count() 이용)

#### getBatchNotifications()
BatchNotifications 테이블에서 인자로 전달받은 ri와 nu 값이 모두 일치하는 객체를 리스트로 반환  (TinyDB Table.search() 이용)

#### removeBatchNotifications()
BatchNotifications 테이블에서 인자로 전달받은 ri와 nu 값이 모두 일치하는 객체를 삭제 (TinyDB Table.remove() 이용)

## Statistics - statistics table 
<img width="354" alt="image" src="https://github.com/leesangwooon/ACME/assets/144790879/0a97fa30-fee6-4c49-ab9a-6fbcc2deb4d5">

#### searchStatistics()
statistics 테이블의 모든 객체를 리스트로 반환(메서드 반환 타입은 JSON)  (TinyDB Table.all() 이용)

#### upsertStatistics()
statistics 테이블에 이미 데이터가 있다면 update(), 데이터가 없다면 insert(). 즉 statistics 테이블에 대한 upsert 수행 (TinyDB Table.update, insert() 이용)

#### purgeStatistics()
statistics 테이블의 모든 객체를 삭제 (TinyDB Table.truncate() 이용)

## Actions - actions table
<img width="347" alt="image" src="https://github.com/leesangwooon/ACME/assets/144790879/eaeb8beb-b4bd-4d06-a65a-b4c2860220c5">

#### searchActionReprs()
action 테이블의 모든 객체를 반환, 테이블이 empty인 경우 none 반환 (TinyDB Table.all() 이용)

#### getAction()
actions 테이블에서 인자로 전달받은 ri에 해당하는 첫 번째 action 객체를 반환 (TinyDB Table.get() 이용)

#### searchActionsDeprsForSubject()
actions 테이블에서 인자로 전달받은 ri에 해당하는 모든 action 객체를 반환  (TinyDB Query(), Table.search() 이용)

#### upsertActionRepr()
ACTR 타입의 action 객체을 인자로 받아 지정된 'ri'에 action을 upsert (TinyDB Table.upsert() 이용)

#### updateActionRepr()
JSON 형식의 actionRepr을 인자로 받아 지정된 'ri'에 update (TinyDB Table.update 이용)

#### removeActionRepr()
actions 테이블에서 인자로 전달받은 ri에 해당하는 action 객체를 조회하고 해당되는 action을 삭제 (TinyDB Table.get/remove() 이용)
삭제 여부 bool 타입으로 반환

## Requests - requests table
<img width="348" alt="image" src="https://github.com/leesangwooon/ACME/assets/144790879/8773b28b-34c3-4d76-a1d2-cc8b9a274a88">

#### insertRequest()
만약 requests 테이블에 저장된 request 수가 maxRequests 이상인 경우, 가장 오래된 request를 삭제 (TinyDB Table.remove() 이용)
requests 테이블에 인자로 받은 request를 추가 (TinyDB Table.insert() 이용)
- 인자로 받은 response JSON 파일에서 rsc 키값이 존재하면 해당 값을, 만약 존재하지 않으면 ResponseStatusCode.UNKNOWN을 테이블의 'rsc' 객체에 저장
- 'req', 'rsp' 객체의 경우 none 이 아닌 경우 저장
- 'ts' 타임 스탬프 정보 저장
request insert 성공 여부를 bool 타입으로 반환

#### getRequests()
존재하는 ri 값이 전달되면 해당 ri에 대한 request를 쿼리하여 반환  (TinyDB Table.search() 이용)
ri값이 특정되거나 존재하지 않을 경우 테이블의 모든 request 반환  (TinyDB Table.all() 이용)

#### deleteRequests()
존재하는 ri 값이 전달되면 해당 ri에 대한 request 리소스 remove (TinyDB Table.remove() 이용)
ri값이 특정되거나 존재하지 않을 경우 request 테이블 전체 remove (TinyDB Table.truncate() 이용)

## Schedules - schedules table
<img width="348" alt="image" src="https://github.com/leesangwooon/ACME/assets/144790879/a827561c-b13b-4046-8637-a174680025c8">

#### getSchedules(self)
schedules 테이블의 모든 객체를 리스트로 반환   (TinyDB Table.all() 이용)

#### getSchedule(self, ri:str)
schedules 테이블에서 인자로 전달받은 ri에 해당하는 첫 번째 schedule 객체를 반환 (TinyDB Table.get() 이용)

#### searchSchedules()
schedules table에서 인자로 전달받은 pi에 대한 모든 schedule을 쿼리하여 리스트로 반환 (TinyDB Query(), Table.search() 이용)

#### upsertSchedule()
JSON 형식의 actionRepr 내 'ri' 키에 대응하는 리소스의 schedule을 update (TinyDB Table.update() 이용)

#### removeSchedule()
schedules 테이블에서 인자로 전달받은 ri에 해당하는 schedule을 삭제한 후, 삭제 여부를 bool로 반환 (TinyDB Table.remove() 이용)
