from datetime import datetime, timedelta

from jose import jwt

from src.config import config


class JwtHandler:

    @classmethod
    def create_access_token(cls, uid: str, data: dict = None) -> str:

        now = datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(config.ACCESS_TOKEN_EXPIRE_MINUTES),
            'sub': uid,
            'user': data
        }
        token = jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return token

    @classmethod
    def decode_access_token(cls, token: str):
        try:
            encoded_jwt = jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        except jwt.JWTError:
            return None
        return encoded_jwt


