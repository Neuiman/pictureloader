from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.picture.router import router as pict_router
from src.auth.router import router as auth_router
app = FastAPI()


app.include_router(pict_router,
                   prefix="/picture",
                   tags=["picture"])

app.include_router(auth_router,
                   prefix="/auth",
                   tags=["auth"])

app.mount('/media', StaticFiles(directory='src/media'), name='media')


