from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status

from src.core.jwt_handler import JwtHandler


class Password:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hash_str: str) -> bool:
        return self.pwd_context.verify(password, hash_str)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            token = JwtHandler().decode_access_token(credentials.credentials)
            if token is None:
                return
            return credentials.credentials
        else:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth token")
