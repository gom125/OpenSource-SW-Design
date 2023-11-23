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

HttpServer
	_run 메서드를 통해 서버를 실행 > 각종 req들을 _handleRequest 메서드를 통해 핸들링
 ''' Python
 
	def _run(self) -> None:
		WSGIRequestHandler.protocol_version = "HTTP/1.1"

		# Run the http server. This runs forever.
		# The server can run single-threadedly since some of the underlying
		# components (e.g. TinyDB) may run into problems otherwise.
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
	...
    '''
	_handleRequest 에서 _dissectHttpRequest 함수는 아마도 HTTP 요청을 받아들여 필요한 정보를 추출하고, 해당 요청을 처리하기 위해 내부적으로 필요한 데이터를 구성
 	_dissectHttpRequest(self, request:Request, operation:Operation, path:str) -> Result:

예를 들어, HTTP 요청의 본문(body)에 있는 데이터를 추출하거나, 요청된 경로(path)를 분석하여 필요한 작업(operation)을 식별하고 이에 따라 필요한 처리를 진행할 수 있습니다. 이 과정에서 분석된 결과는 dissectResult에 저장되고, 이후의 로직에서 이를 활용하여 요청을 처리하고 응답을 생성할 수 있게 됩니다.









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




