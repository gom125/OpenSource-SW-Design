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
    
_handleRequest 에서 _dissectHttpRequest 함수는 아마도 HTTP 요청을 받아들여 필요한 정보를 추출하고, 해당 요청을 처리하기 위해 내부적으로 필요한 데이터를 구성

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

toData: 결과 데이터를 특정한 직렬화 타입에 따라 문자열이나 바이트, 혹은 JSON으로 변환하여 반환하는 메서드
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


prepareResultFromRequest: 원본 요청으로부터 필요한 필드를 복사하는 메서드

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




CSE
HttpServer





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




