from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from jose.exceptions import JWTError
from .schema import AuthModel
from datetime import timedelta, datetime
from passlib.hash import bcrypt

router = APIRouter(prefix='/auth')
oauth = OAuth2PasswordBearer(tokenUrl='auth/login')

SECRET_KEY = 'afeojroewirweadfewrw'


@router.post('/register')
async def register(name: str, password: str):
    user = await AuthModel.get_or_none(name=name)

    if user:
        raise HTTPException(409, 'User is alreay existed')

    await AuthModel.create(name=name, password_hash=bcrypt.hash(password))

    return {
        'code': 200,
        'message': 'register success!',
    }


@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await AuthModel.get_or_none(name=form.username)

    if not user:
        raise HTTPException(401, detail='No such user')

    now = datetime.utcnow()

    if bcrypt.verify(form.password, user.password_hash):
        token = jwt.encode({
            'iat': now,
            'exp': now + timedelta(days=1),
            'name': form.username,
            'id': user.id
        }, SECRET_KEY)

        return {
            'access_token': token,
            'token_type': 'Bearer'
        }
    else:
        raise HTTPException(401, detail='Incorrect username or password')


@router.get('/me')
async def get_current_user(token: str = Depends(oauth)):
    try:
        user = jwt.decode(token, SECRET_KEY)
    except JWTError:
        raise HTTPException(401, 'Auth expired')

    return user
