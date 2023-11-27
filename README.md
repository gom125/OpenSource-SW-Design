# Analysis

# What is ACME?
ACME (An open source CSE Middleware for Education)

oneM2M architecture has two basic Entity
1. AE (Application Entity)
2. CSE (Common Services Entity)

<img src="http://www.onem2m.org/images/app_dev_guide/ArchImg.png">

AE (Light, Smartphone)
CSE (Home Gateway, Cloud Service Platform)

oneM2M's entities communicate via a RESTful req-res protocol
> Mca: AE connect with CSE
> MCC: CSE connect with CSE

Possible flows are:
AE > CSE
CSE > AE or CSE
we need those flows protocol bindings.

ACME Protocol Bindings and Serializations
Protocols Bindings
- http
- MQTT

Serializations
- JSON
- CBOR


# Request Flow in ACME
HttpServer.py
MQTTClient.py

1. HttpServer.py 에서 서버를 실행시키고 _handleRequest 메서드를 http 프로토콜 통해 핸



Request received: By http or mqtt

Class HttpServer
_run 메서드를 통해 서버를 실행 > 각종 req들을 _handleRequest 메서드를 통해 핸들링

	def _run(self) -> None:
		WSGIRequestHandler.protocol_version = "HTTP/1.1"
		if self.flaskApp:
			# Disable the flask banner messages
			cli = sys.modules['flask.cli']
			cli.show_server_banner = lambda *x: None 	# type: ignore
			# Start the server
			try:
				if self.wsgiEnable:
					L.isInfo and L.log(f'HTTP server listening on {self.listenIF}:{self.port} (wsgi)')
					serve(self.flaskApp, 
		   				  host = self.listenIF, 
						  port = self.port, 
						  threads = self.wsgiThreadPoolSize, 
						  connection_limit = self.wsgiConnectionLimit)
    
_handleRequest 에서 _dissectHttpRequest 함수는 HTTP 요청을 받아들여 필요한 정보를 추출하고, 해당 요청을 처리하기 위해 내부적으로 필요한 데이터를 구성

	def _handleRequest(self, path:str, operation:Operation) -> Response:
		"""	Get and check all the necessary information from the request and
			build the internal strutures. Then, depending on the operation,
			call the associated request handler.
		"""
		L.isDebug and L.logDebug(f'==> HTTP Request: {path}') 	# path = request.path  w/o the root
		L.isDebug and L.logDebug(f'Operation: {operation.name}')
		L.isDebug and L.logDebug(f'Headers: \n{str(request.headers).rstrip()}')
		try:
			dissectResult = self._dissectHttpRequest(request, operation, path)
		except ResponseException as e:
			dissectResult = Result(rsc = e.rsc, request = e.data, dbg = e.dbg)


_dissectHttpRequest(self, request:Request, operation:Operation, path:str) -> Result:

여기서 _dissectHttpRequest를 통해 request 값이 Result 데이터 클래스의 값으로 변하게 되는데,

Result 이 클래스는 함수들이 반환하는 일반적인 결과 상태를 나타내며, 여러 정보를 포함할 수 있습니다. 이 클래스의 속성은 다양한 종류의 데이터를 저장할 수 있도록 구성되어 있습니다.

resource: 리소스 객체를 담는 속성
data: 데이터 혹은 데이터 시퀀스를 담는 속성
rsc: 응답 상태 코드를 담는 속성
dbg: 디버그 메시지를 담는 속성
request: CSERequest 객체를 담는 속성
embeddedRequest: 내장된 CSERequest 객체를 담는 속성
주요 메서드:
1. toData: 결과 데이터를 특정한 직렬화 타입에 따라 문자열이나 바이트, 혹은 JSON으로 변환하여 반환하는 메서드
serializeData() 메서드를 사용해서 resource를 직렬화 시킴.

	if isinstance(self.resource, Resource):
				r = serializeData(self.resource.asDict(), ct)
			elif self.dbg:
				r = serializeData({ 'm2m:dbg' : self.dbg }, ct)
			elif isinstance(self.resource, dict):
				r = serializeData(self.resource, ct)
			elif self.data:									# explicit json or cbor from the dict
				r = serializeData(cast(JSON, self.data), ct)
			elif self.request and self.request.pc:		# Return the dict if the request is set and has a dict
				r = self.request.pc
			else:
				r = ''
			return r


2. prepareResultFromRequest: 원본 요청으로부터 필요한 필드를 복사하는 메서드

-----

serializeData 메서드
		
		def serializeData(data:JSON, ct:ContentSerializationType) -> Optional[str|bytes|JSON]:
			"""	Serialize a dictionary, depending on the serialization type.
		
				Args:
					data: The data to serialize.
					ct: The *data* content serialization format.
				
				Return:
					A data *str* or *byte* object with the serialized data, or *None*.
			"""
			if ct == ContentSerializationType.PLAIN:
				return data
			encoder = json if ct == ContentSerializationType.JSON else cbor2 if ct == ContentSerializationType.CBOR else None
			if not encoder:
				return None
			return encoder.dumps(data)	# type:ignore[no-any-return]
		
		
		def deserializeData(data:bytes, ct:ContentSerializationType) -> Optional[JSON]:
			"""	Deserialize data into a dictionary, depending on the serialization type.
		
				Args:
					data: The data to deserialize.
					ct: The *data* content serialization format.
				
				Return:
					If the *data* is not *None*, but has a length of 0 then an empty dictionary is returned. If an unknown content serialization is specified then *None* is returned. Otherwise, a `JSON` object is returned.
			"""
			if len(data) == 0:
				return {}
			match ct:
				case ContentSerializationType.JSON:
					return cast(JSON, json.loads(TextTools.removeCommentsFromJSON(data.decode('utf-8'))))
				case ContentSerializationType.CBOR:
					return cast(JSON, cbor2.loads(data))
				case _:
					return None





Flow

acme 실행시 cse에서 flaskApp에 서버 run 시킴
> 서버 flaskApp에 http request가 들어옴.
> flaskApp에 Endpoint에 메서드별로 따로 http가 나뉨.
이때 메서드별로 해당 요청의 기능에 따라 operation enum 클래스를 정해주고

Operation Enum
Create, Retrieve, Update, Delete, Notify, Discovery, Na

> 해당하는 Operation에 따라 _handleRequest를 실행
_handleRequest에는
	dissectHttpRequest라는 메서드를 통해 데이터를 Result 타입으로 변환
	Dissect an HTTP request. Combine headers and contents into a single structure. Result is returned in Result.request.

이때 cseRequest()를 생성시켜 
Result 타입으로 반환한다.

Result 클래스는 cseRequest의 값들에서 def toData(self, ct:Optional[ContentSerializationType] = None) -> str|bytes|JSON:
메서드랑 prepareResultFromRequest 메서드가 추가된 것이다.

> Result타입의 반환된 값을 cse.request.handleRequest에게 넘긴다.
cse.request에서 handlerequest에서는 Operation에 따라 cse.dispatcher에 process~~ 메서드를 호출하여 실질적인 req를 처리하게끔 한다.
이때 createLocalResource, update~,, 등의 작업으로 cse.storage에 db.createResource ,,, 등의 CURD 작업을 호출,, 결과 tinyDB에 데이터를 저장하게 된다.



Flow


HttpServer

_run 메서드

flaskApp 서버 실행	addEndpoint로 flaskApp.add_url_rule로 메서드별(GET, POST, PUT, DELETE 에 따라)로 받는 Endpoint 추가 

Endpoint에 요청 들어오면 _handleRequest 메서드에서 dissectHttpRequest 메서드 실행

dissectHttpRequest(request, operation) -> Result
request 데이터랑 operation(http method enum 클래스) 받아서 
request 데이터를 CSERequest 형태로 변환 
리턴값 > Result(request = CSERequest) 

Result클래스 를 반환

Result 클래스에 toData메서드 resource 값을 serializeData() 하



TinyDB

실질적인 데이터베이스 로직 python으로 테이블 생성 및 CRUD

    """ This class implements the TinyDB binding to the database. It is used by the Storage class.
    """
 
CRUD
C = insertResource(Resource, ri)
R = searchResource(ri,csi,srn,pi,ty,aei) -> list[Document]
U = updateResource(Resource, ri)
D = deleteResource(Resource)

> Storage(storage.createResource) > 
""" This module defines storage managers and drivers for database access.

    Storage managers are used to store, retrieve and manage resources and other runtime data in the database.

    Storage drivers are used to access the database. Currently, the only supported database is TinyDB.

    See also:
        - `TinyDBBetterTable`
        - `TinyDBBufferedStorage`
"""

C = createResource(self, resource:Resource, overwrite:Optional[bool] = True) -> None:
R = retrieveResource(self, ri:Optional[str] = None, 
                                csi:Optional[str] = None,
                                srn:Optional[str] = None, 
                                aei:Optional[str] = None) -> Resource:

U = updateResource(self, resource:Resource) -> Resource:
D = deleteResource(self, resource:Resource) -> None:

> Resource(object)
    """ Base class for all oneM2M resource types,
    
        Attributes:

    """

    __slots__ = (
        'tpe',
        'readOnly',
        'inheritACP',
        'dict',
        'isImported',
        '_originalDict',
    )

    _excludeFromUpdate = [ 'ri', 'ty', 'pi', 'ct', 'lt', 'st', 'rn', 'mgd' ]
    """ Resource attributes that are excluded when updating the resource """

C = dbCreate(self, overwrite:Optional[bool] = False) -> None:
R = dbReload(self) -> Resource:
U = dbUpdate(self, finalize:bool = False) -> Resource:
D = dbDelete(self) -> None:

> Dispatcher

Dispatch request to operation handler

""" Dispatcher class. Handles all requests and dispatches them to the
        appropriate handlers. This includes requests for resources, requests
        for resource creation, and requests for resource deletion.
    """

C = def createLocalResource(self,
                            resource:Resource,
                            parentResource:Resource,
                            originator:Optional[str] = None,
                            request:Optional[CSERequest] = None) -> Resource:

processCreateRequest > createLocalResource
createResourceFromDict > createLocalResource

R

U = def updateLocalResource(self, resource:Resource, 
                                  dct:Optional[JSON] = None, 
                                  doUpdateCheck:Optional[bool] = True, 
                                  originator:Optional[str] = None) -> Resource:


D = processDeleteRequest(self, request:CSERequest, 
                                   originator:str, 
                                   id:Optional[str] = None) -> Result:

> RequestManager

        # Map request handlers and events for operations in the RequestManager and the dispatcher

def handleRequest(self, request:Union[CSERequest, JSON]) -> Result:


self.requestHandlers:RequestHandler = {       
            Operation.RETRIEVE  : RequestCallback(self.retrieveRequest, 
                                                  CSE.dispatcher.processRetrieveRequest, 
                                                  self._sendRequest,
                                                  self._eventHttpSendRetrieve,
                                                  self._eventMqttSendRetrieve),
                                                #   self.sendRetrieveRequest),
            Operation.DISCOVERY : RequestCallback(self.retrieveRequest, 
                                                  CSE.dispatcher.processRetrieveRequest, 
                                                  self._sendRequest,
                                                  self._eventHttpSendRetrieve,
                                                  self._eventMqttSendRetrieve),
                                                #   self.sendRetrieveRequest),
            Operation.CREATE    : RequestCallback(self.createRequest,
                                                  CSE.dispatcher.processCreateRequest,
                                                  self._sendRequest,
                                                  self._eventHttpSendCreate,
                                                  self._eventMqttSendCreate),
                                                #   self.sendCreateRequest),
            Operation.UPDATE    : RequestCallback(self.updateRequest,
                                                  CSE.dispatcher.processUpdateRequest,
                                                  self._sendRequest,
                                                  self._eventHttpSendUpdate,
                                                  self._eventMqttSendUpdate),
                                                #   self.sendUpdateRequest),
            Operation.DELETE    : RequestCallback(self.deleteRequest,
                                                  CSE.dispatcher.processDeleteRequest,
                                                  self._sendRequest,
                                                  self._eventHttpSendDelete,
                                                  self._eventMqttSendDelete),
                                                #   self.sendDeleteRequest),
            Operation.NOTIFY    : RequestCallback(self.notifyRequest,
                                                  CSE.dispatcher.processNotifyRequest,
                                                  self._sendRequest,
                                                  self._eventHttpSendNotify,
                                                  self._eventMqttSendNotify),
                                                #   self.sendNotifyRequest),
        }

C = createRequest(self, request:CSERequest) -> Result:
R
U = updateRequest(self, request:CSERequest) -> Result:
D = deleteRequest(self, request:CSERequest,) -> Result:

> HttpServer

HttpServer.py에서 flask App을 통해 서버를 열고
각각 메서드 마다 _handleRequest(메서드별로) endpoint 연결




dissectResult = self._dissectHttpRequest(request, operation, path)

_dissectHttpRequest > Validator > CSERequest

responseResult = CSE.request.handleRequest(dissectResult.request)


http > request > CSERequest > Result 







# 1.CSE.py
CSE(Common Service Entity) 제공 공통 기능
데이터 관리 : 데이터 저장 및 관리, 데이터 분석 기능

global storage = Storage()

# 2.Storage.py

1) Storage Class 
DB에 저장하는 entry points

__slots__ = (인스턴스 고정 속성)
https://ddanggle.gitbooks.io/interpy-kr/content/ch10-slots-magic.html

__init__ = 

2) TinyDBBinding Class

__slots__ =  (
    path : 
)

__init__(self, path: str, postfix:str) = {
    #path : Path to the database directory
    #posfix : Postfix for the database file names.

    #path 설정
    self.path = path

    #연결 Config()
    self._assignConfig()


}


	def _assignConfig(self) -> None:
		"""	Assign default configurations.
		"""
		self.cacheSize = Configuration.get('database.cacheSize')
		""" Size of the cache for the TinyDB tables. """
		self.writeDelay = Configuration.get('database.writeDelay')
		""" Delay for writing to the database. """
		self.maxRequests = Configuration.get('cse.operation.requests.size')
		""" Maximum number of oneM2M recorded requests to keep in the database. """




