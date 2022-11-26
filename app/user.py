from datetime import datetime, timedelta
from typing import Optional
import jwt

from attrdict import AttrDict
from fastapi import FastAPI, Header, Cookie, Response
from pydantic import BaseModel

from app import db_manager

app = FastAPI()
encryption_secret = "secrete"
algorithm = "HS256"


class User(BaseModel):
    user_id: str
    password: str


class ResponseData(BaseModel):
    code: int
    data: Optional[str] = None


@app.get('/')
def register_user():
    return {'수완치를 위한': '간단 토큰'}


@app.post('/register', response_model=ResponseData)
def register_user(user: User):
    user = AttrDict(user)

    already_user = db_manager.select_user(user_id=user.user_id)

    # 중복 이메일 처리
    if already_user:
        return ResponseData(code=2001, data='이미 존재하는 아이디 입니다.')

    try:
        db_manager.insert_user(user_id=user.user_id, password=user.password)

    except:
        ResponseData(code=5001, data='서버 오류')

    return ResponseData(code=2000, data="성공")


@app.post('/check_pw', response_model=ResponseData)
def check_password(user: User):
    user = AttrDict(user)

    # 존재하지 않는 이메일 확인
    already_user = db_manager.select_user(user_id=user.user_id, scalar=True)

    # 중복 이메일 처리
    if not already_user:
        return ResponseData(code=2002, data='존재하지 않는 이메일입니다.')

    if user.password == already_user.password:
        return ResponseData(code=2000, data='비밀번호가 일치합니다.')

    else:
        return ResponseData(code=2003, data='비밀번호가 일치하지 않습니다.')


@app.post('/login', response_model=ResponseData)
def login(user: User, response: Response):
    user = AttrDict(user)

    # 존재하지 않는 이메일 확인
    already_user = db_manager.select_user(user_id=user.user_id, scalar=True)

    # 중복 이메일 처리
    if not already_user:
        return ResponseData(code=2002, data='존재하지 않는 이메일입니다.')

    if user.password == already_user.password:
        response.set_cookie('jwt_token', jwt_encode(user), samesite=None, secure=True)
        return ResponseData(code=2000, data='성공.')

    else:
        return ResponseData(code=2003, data='비밀번호가 일치하지 않습니다.', token_header='test')


def jwt_encode(data: dict):
    data['exp'] = datetime.now() + timedelta(minutes=10)
    return jwt.encode(data, encryption_secret, algorithm=algorithm)


def jwt_decode(jwt_data: str):
    return jwt.decode(jwt_data, encryption_secret, algorithms=[algorithm])



