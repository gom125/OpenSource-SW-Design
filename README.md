# Analysis


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




