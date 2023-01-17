from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import user_router, auth_router, post_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_app():
    app = FastAPI(
        title="Users App",
        description="Handling Our Users",
        version="1",
    )

    @app.on_event("startup")
    async def startup():
        pass

    @app.on_event("shutdown")
    async def shutdown():
        pass

    app.include_router(
        auth_router.router
    )
    app.include_router(
        user_router.router
    )
    app.include_router(
        post_router.router
    )
    return app


app = init_app()


