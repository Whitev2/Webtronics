from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
import uvicorn
import rsa

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def encrypt_1(link_str: str) -> str:
    """
    Method 1
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(link_str)


def encrypt_2(link_str: str):
    """
    Method 2
    """

    pubkey, privkey = rsa.newkeys(512)

    enctex = rsa.encrypt(link_str.encode(), pubkey)  # Шифрование выполняется с помощью публичного ключа
    dectex = rsa.decrypt(enctex, privkey).decode()  # Дешифрование выполняется с помощью приватного ключа

    return enctex.hex()


@app.router.post("/{link_str}")
def encrypt_str(link_str) -> dict:
    return {"Method 1": encrypt_1(link_str), "Method 2": encrypt_2(link_str)}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8001)


if __name__ == '__main__':
    main()
