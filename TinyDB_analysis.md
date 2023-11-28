총 정리


TinyDB

테이블 8개
- Resources
- Indentifiers
- Subscriptions
- BatchNotifications
- Statistics
- Actions
- Requests
- Schedules

* 		Resources
    * insertResource: 리소스 추가
    * upsertResource: 리소스 업데이트 또는 삽입
    * updateResource: 리소스 업데이트
    * deleteResource: 리소스 삭제
    * searchResources: 리소스 검색
    * discoverResourcesByFilter: 필터로 리소스 검색
    * hasResource: 리소스 유무 확인
    * countResources: 리소스 개수 확인
    * searchByFragment: 조각으로 검색

* 		Identifiers, Structured RI, Child Resources
    * upsertIdentifier: 식별자 업데이트 또는 삽입
    * deleteIdentifier: 식별자 삭제
    * searchIdentifiers: 식별자 검색
    * upsertChildResource: 자식 리소스 업데이트 또는 삽입
    * removeChildResource: 자식 리소스 삭제
    * searchChildResourcesByParentRI: 부모 리소스로 자식 리소스 검색

* 		Subscriptions
    * searchSubscriptions: 구독 검색
    * upsertSubscription: 구독 업데이트 또는 삽입
    * removeSubscription: 구독 삭제

* 		BatchNotifications
    * addBatchNotification: 배치 알림 추가
    * countBatchNotifications: 배치 알림 개수 확인
    * getBatchNotifications: 배치 알림 가져오기
    * removeBatchNotifications: 배치 알림 삭제

* 		Statistics
    * searchStatistics: 통계 검색
    * upsertStatistics: 통계 업데이트 또는 삽입
    * purgeStatistics: 통계 삭제

* 		Actions
    * searchActionReprs: 액션 검색
    * getAction: 액션 가져오기
    * searchActionsDeprsForSubject: 주제별 액션 검색
    * upsertActionRepr: 액션 삽입 또는 업데이트
    * updateActionRepr: 액션 업데이트
    * removeActionRepr: 액션 삭제

* 		Requests
    * insertRequest: 요청 삽입
    * getRequests: 요청 가져오기
    * deleteRequests: 요청 삭제

* 		Schedules
    * getSchedules: 스케줄 가져오기
    * getSchedule: 스케줄 가져오기
    * searchSchedules: 스케줄 검색
    * upsertSchedule: 스케줄 삽입 또는 업데이트
    * removeSchedule: 스케줄 삭제


1. Resources
* 		insertResource(resource: Resource, ri: str) -> None:
    * 데이터베이스에 리소스를 삽입합니다. resource는 삽입할 리소스이고, ri는 리소스의 ID입니다.

* 		upsertResource(resource: Resource, ri: str) -> None:
    * 리소스를 업데이트하거나 데이터베이스에 삽입합니다. 이미 존재하는 경우 업데이트하고, 존재하지 않는 경우 새로운 리소스를 삽입합니다.

* 		updateResource(resource: Resource, ri: str) -> Resource:
    * 데이터베이스에서 리소스를 업데이트합니다. None이 아닌 필드만 업데이트합니다.

* 		deleteResource(resource: Resource) -> None:
    * 데이터베이스에서 리소스를 삭제합니다.

* 		searchResources(ri: Optional[str] = None, csi: Optional[str] = None, srn: Optional[str] = None, pi: Optional[str] = None, ty: Optional[int] = None, aei: Optional[str] = None) -> list[Document]:
    * 리소스를 구조화된 리소스 이름, 리소스 ID, CSE-ID, 부모 리소스 ID, 리소스 유형 또는 애플리케이션 엔터티 ID로 검색합니다.

* 		discoverResourcesByFilter(func: Callable[[JSON], bool]) -> list[Document]:
    * 필터 함수에 따라 리소스를 검색합니다.

* 		hasResource(ri: Optional[str] = None, csi: Optional[str] = None, srn: Optional[str] = None, ty: Optional[int] = None) -> bool:
    * 데이터베이스에 리소스가 있는지 확인합니다.

* 		countResources() -> int:
    * 데이터베이스 내의 리소스 개수를 반환합니다.

* 		searchByFragment(dct: dict) -> list[Document]:
    * 주어진 딕셔너리 또는 문서와 일치하는 모든 리소스를 검색합니다.

이 함수들은 데이터베이스에 리소스를 추가, 업데이트, 삭제하고, 특정 조건에 따라 리소스를 검색하거나 개수를 세는 등의 작업을 수행합니다.


2. Identifiers, Structured RI, Child Resources
* 		upsertIdentifier(resource: Resource, ri: str, srn: str) -> None:
    * Identifiers DB에 식별자를 삽입하거나 업데이트합니다.
    * resource: 삽입할 리소스입니다.
    * ri: 리소스의 ID입니다.
    * srn: 리소스의 구조화된 리소스 이름입니다.

* 		deleteIdentifier(resource: Resource) -> None:
    * Identifiers DB에서 식별자를 삭제합니다.
    * resource: 식별자를 삭제할 리소스입니다.

* 		searchIdentifiers(ri: Optional[str] = None, srn: Optional[str] = None) -> list[Document]:
    * Identifiers DB에서 리소스 ID 또는 구조화된 이름을 검색합니다.
    * ri: 검색할 리소스 ID입니다.
    * srn: 검색할 구조화된 경로입니다.

* 		upsertChildResource(resource: Resource, ri: str) -> None:
    * childResources DB에 자식 리소스를 추가합니다.
    * resource: 자식으로 추가할 리소스입니다.
    * ri: 리소스의 ID입니다.

* 		removeChildResource(resource: Resource) -> None:
    * childResources DB에서 자식 리소스를 제거합니다.
    * resource: 자식으로 추가할 리소스입니다.

* 		searchChildResourcesByParentRI(pi: str, ty: Optional[ResourceTypes | list[ResourceTypes]] = None) -> list[str]:
    * 부모 리소스 ID에 따라 자식 리소스를 검색합니다.
    * pi: 부모 리소스의 ID입니다.
    * ty: 검색할 자식 리소스의 유형 또는 유형 목록입니다.

이 함수들은 Identifiers DB와 childResources DB에서 식별자를 삽입, 업데이트, 삭제하거나, 검색하는 데 사용됩니다. 각각의 역할에 따라서, 리소스의 식별자를 관리하고, 자식 리소스를 조작하며, 부모-자식 관계를 확인하는 데 활용됩니다.

3. Subscriptions
* 		searchSubscriptions(ri: Optional[str] = None, pi: Optional[str] = None) -> Optional[list[Document]]
    * 리소스 ID 또는 부모 리소스 ID에 따라 구독 표현을 검색합니다.
    * ri 또는 pi 중 하나의 매개변수만 사용할 수 있습니다. 우선순위는 리소스 ID 이후에 부모 리소스 ID입니다.
    * 리턴값: 검색된 구독 표현의 목록 또는 None입니다.

* 		upsertSubscription(subscription: Resource) -> bool
    * 구독 표현을 데이터베이스에 업데이트하거나 삽입합니다.
    * subscription: 업데이트 또는 삽입할 구독(SUB)입니다.
    * 리턴값: 구독 표현이 업데이트 또는 삽입되었을 경우 True, 그렇지 않으면 False입니다.

* 		removeSubscription(subscription: Resource) -> bool
    * 데이터베이스에서 구독 표현을 제거합니다.
    * subscription: 제거할 구독(SUB)입니다.
    * 리턴값: 구독 표현이 제거되었을 경우 True, 그렇지 않으면 False입니다.

이 함수들은 각각 Subscriptions 테이블에서 구독을 검색하고 삽입 또는 제거하는 데 사용됩니다. searchSubscriptions는 리소스 ID 또는 부모 리소스 ID를 기반으로 검색하며, upsertSubscription은 구독을 업데이트하거나 새로 삽입하고, removeSubscription은 구독을 제거합니다.

4. BatchNotifications
* 		addBatchNotification(ri: str, nu: str, notificationRequest: JSON) -> bool:
    * ri: 리소스 ID입니다.
    * nu: 알림 URI입니다.
    * notificationRequest: 알림 요청입니다.
    * 이 함수는 배치 알림을 데이터베이스에 추가합니다. ri, nu, notificationRequest 정보를 사용하여 새로운 배치 알림을 생성하고 데이터베이스에 추가합니다. 추가된 경우 True를 반환하고, 그렇지 않은 경우 False를 반환합니다.

* 		countBatchNotifications(ri: str, nu: str) -> int:
    * ri: 리소스 ID입니다.
    * nu: 알림 URI입니다.
    * 이 함수는 특정 리소스와 알림 URI에 대한 배치 알림의 수를 반환합니다. 지정된 ri와 nu에 해당하는 배치 알림의 총 개수를 정수형으로 반환합니다.

* 		getBatchNotifications(ri: str, nu: str) -> list[Document]:
    * ri: 리소스 ID입니다.
    * nu: 알림 URI입니다.
    * 이 함수는 특정 리소스와 알림 URI에 대한 배치 알림을 조회합니다. 지정된 ri와 nu에 해당하는 배치 알림을 문서(Document) 형태의 리스트로 반환합니다.

* 		removeBatchNotifications(ri: str, nu: str) -> bool:
    * ri: 리소스 ID입니다.
    * nu: 알림 URI입니다.
    * 이 함수는 특정 리소스와 알림 URI에 대한 배치 알림을 제거합니다. ri와 nu에 해당하는 배치 알림을 데이터베이스에서 삭제하며, 삭제가 이루어진 경우 True를 반환하고, 그렇지 않은 경우 False를 반환합니다.

이 함수들은 배치 알림과 관련된 데이터베이스 조작을 수행합니다. 새로운 배치 알림을 추가하거나, 해당 알림의 수를 확인하고 조회하며, 필요한 경우 배치 알림을 삭제합니다.


5. Statistics
* 		searchStatistics() -> JSON:
    * 이 함수는 통계 정보를 검색합니다.
    * 반환 값: 통계 정보를 반환하며, 정보가 없으면 None을 반환합니다.

* 		upsertStatistics(stats: JSON) -> bool:
    * 이 함수는 통계 정보를 업데이트하거나 삽입합니다.
    * stats: 업데이트하거나 삽입할 통계 정보입니다.
    * 반환 값: 통계 정보가 업데이트되거나 삽입되면 True를 반환하고, 그렇지 않으면 False를 반환합니다.

* 		purgeStatistics() -> None:
    * 이 함수는 통계 데이터베이스를 초기화하여 데이터를 모두 삭제합니다.

이 함수들은 통계 정보를 조회하거나 업데이트하고, 필요한 경우 통계 데이터베이스를 초기화하여 모든 정보를 삭제합니다. 특히 upsertStatistics() 함수는 통계 정보를 업데이트하거나 새로운 정보를 추가하는데 사용됩니다. 만약 기존에 정보가 있다면 업데이트하고, 없다면 새로운 정보를 추가합니다.


6. Actions
* 		searchActionReprs() -> list[Document]:
    * 액션 표현들을 검색합니다.
    * 반환 값: 액션 표현들의 리스트를 반환하며, 검색 결과가 없으면 None을 반환합니다.

* 		getAction(ri: str) -> Optional[Document]:
    * 리소스 ID로 액션 표현을 가져옵니다.
    * ri: 액션 표현의 리소스 ID입니다.
    * 반환 값: 해당 액션 표현을 반환하며, 없을 경우 None을 반환합니다.

* 		searchActionsDeprsForSubject(ri: str) -> Sequence[JSON]:
    * 주체별로 액션 표현들을 검색합니다.
    * ri: 액션 표현 주체의 리소스 ID입니다.
    * 반환 값: 주어진 주체에 대한 액션 표현들의 리스트를 반환하며, 없을 경우 None을 반환합니다.

* 		upsertActionRepr(action: ACTR, periodTS: float, count: int) -> bool:
    * 액션 표현을 업데이트하거나 삽입합니다.
    * action: 업데이트하거나 삽입할 액션 표현입니다.
    * periodTS: 주기적 실행을 위한 타임스탬프입니다.
    * count: 액션이 실행될 횟수입니다.
    * 반환 값: 액션 표현이 성공적으로 업데이트 또는 삽입되면 True를 반환하고, 그렇지 않으면 False를 반환합니다.

* 		updateActionRepr(actionRepr: JSON) -> bool:
    * 액션 표현을 업데이트합니다.
    * actionRepr: 업데이트할 액션 표현입니다.
    * 반환 값: 액션 표현이 성공적으로 업데이트되면 True를 반환하고, 그렇지 않으면 False를 반환합니다.

* 		removeActionRepr(ri: str) -> bool:
    * 액션 표현을 제거합니다.
    * ri: 액션의 리소스 ID입니다.
    * 반환 값: 액션 표현이 성공적으로 제거되면 True를 반환하고, 그렇지 않으면 False를 반환합니다.

이 함수들은 액션 표현을 검색하거나 업데이트하고, 필요한 경우 삭제합니다. 특히 upsertActionRepr() 함수는 액션 표현을 업데이트하거나 삽입하는 데 사용됩니다. 만약 기존에 정보가 있다면 업데이트하고, 없다면 새로운 정보를 추가합니다.

7. Requests
* 		insertRequest(op: Operation, ri: str, srn: str, originator: str, outgoing: bool, ot: str, request: JSON, response: JSON) -> bool:
    * 요청을 requests 데이터베이스에 추가합니다.
    * op: 작업(Operation)입니다.
    * ri: 요청 대상 리소스의 리소스 ID입니다.
    * srn: 요청 대상 리소스의 구조화된 리소스 ID입니다.
    * originator: 요청의 발신자입니다.
    * outgoing: 참일 경우, CSE에서 보낸 요청입니다.
    * ot: 요청 생성 타임스탬프입니다.
    * request: 저장할 요청입니다.
    * response: 저장할 응답입니다.
    * 반환 값: 성공 또는 실패를 나타내는 부울 값입니다.

* 		getRequests(ri: Optional[str] = None) -> list[Document]:
    * 리소스 ID에 대한 요청 또는 모든 요청을 가져옵니다.
    * ri: 대상 리소스의 리소스 ID입니다. None 또는 빈 경우 모든 요청이 반환됩니다.
    * 반환 값: 요청들의 리스트인 Documents를 반환하며, 비어있을 수 있습니다.

* 		deleteRequests(ri: Optional[str] = None) -> None:
    * 데이터베이스에서 저장된 모든 요청을 제거합니다.
    * ri: 선택적인 리소스 ID입니다. 해당 리소스 ID에 대한 요청만 삭제됩니다.

insertRequest() 함수는 요청을 데이터베이스에 추가합니다. 먼저 최대 요청 수에 도달했는지 확인하고, 도달한 경우 가장 오래된 요청을 삭제합니다. 그런 다음 요청 및 응답에 대한 정보를 준비하고, 이 정보를 요청 데이터베이스에 추가합니다.
getRequests() 함수는 특정 리소스 ID에 해당하는 요청을 가져오거나, 모든 요청을 반환합니다. 리소스 ID가 지정되지 않은 경우 모든 요청이 반환됩니다.
deleteRequests() 함수는 데이터베이스에서 저장된 모든 요청을 삭제합니다. 선택적으로 특정 리소스 ID에 대한 요청만 삭제할 수 있습니다.


8. Schedules
* 		getSchedules() -> list[Document]:
    * 데이터베이스에서 모든 스케줄을 가져옵니다.
    * 반환 값: Documents의 리스트를 반환하며, 비어있을 수 있습니다.

* 		getSchedule(ri: str) -> Optional[Document]:
    * 데이터베이스에서 특정 스케줄을 가져옵니다.
    * ri: 스케줄의 리소스 ID입니다.
    * 반환 값: 해당하는 스케줄을 반환하거나 없는 경우 None을 반환합니다.

* 		searchSchedules(pi: str) -> list[Document]:
    * 데이터베이스에서 스케줄을 검색합니다.
    * pi: 부모 리소스의 리소스 ID입니다.
    * 반환 값: Documents의 리스트를 반환하며, 비어있을 수 있습니다.

* 		upsertSchedule(ri: str, pi: str, schedule: list[str]) -> bool:
    * 데이터베이스에 스케줄을 추가하거나 업데이트합니다.
    * ri: 스케줄의 리소스 ID입니다.
    * pi: 스케줄의 부모 리소스 ID입니다.
    * schedule: 저장할 스케줄입니다.
    * 반환 값: 스케줄이 추가 또는 업데이트되었으면 True, 그렇지 않으면 False를 반환합니다.

* 		removeSchedule(ri: str) -> bool:
    * 데이터베이스에서 스케줄을 제거합니다.
    * ri: 제거할 스케줄의 리소스 ID입니다.
    * 반환 값: 스케줄이 성공적으로 제거되면 True, 그렇지 않으면 False를 반환합니다.

getSchedules() 함수는 데이터베이스에서 모든 스케줄을 가져옵니다. getSchedule() 함수는 특정 리소스 ID에 해당하는 스케줄을 가져옵니다. searchSchedules() 함수는 부모 리소스 ID에 해당하는 스케줄을 검색합니다. upsertSchedule() 함수는 스케줄을 추가하거나 업데이트합니다. removeSchedule() 함수는 데이터베이스에서 스케줄을 제거합니다.
