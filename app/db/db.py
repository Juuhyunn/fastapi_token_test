from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_info = {
    # 데이터베이스에 접속할 사용자 아이디
    'user': 'root',
    # 사용자 비밀번호
    'password': 'root',
    # 접속할 데이터베이스의 주소 (같은 컴퓨터에 있는 데이터베이스에 접속하기 때문에 localhost)
    'host': 'localhost',
    # 관계형 데이터베이스는 주로 3306 포트를 통해 연결됨
    'port': 3306,
    # 실제 사용할 데이터베이스 이름
    'database': 'juu_simple'
}

DB_URL = f"mysql+pymysql://{db_info['user']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['database']}?charset=utf8"


class DBConnect:
    def __init__(self):
        self.engine = create_engine(DB_URL, echo=True)

    def session_maker(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def connection(self):
        conn = self.engine.connect()
        return conn


session = DBConnect().session_maker()