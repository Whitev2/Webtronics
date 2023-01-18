from datetime import datetime, timedelta
from jose import jwt

from src.config import config


class JwtHandler:

    @classmethod
    def create_access_token(cls, uid: str, data: dict = None) -> str:
        """
        This function allows you to create a jwt token based on data

        uid: user_id
        data: data dictionary
        """

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
        """
        This function decrypts a jwt token

        token: jwt
        """
        try:
            encoded_jwt = jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        except jwt.JWTError:
            return None
        return encoded_jwt