import asyncio
import io
from contextlib import asynccontextmanager

from fastapi import UploadFile, FastAPI, File, Depends
from fastapi.responses import StreamingResponse

from src.consumer import consume
from src.pictureprocessorcervice import PictureService, create_picture_service




@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(consume())
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/process")
async def process_image(picture_service: PictureService = Depends(create_picture_service), file: UploadFile = File(...)):
    processed_image = await picture_service.process_image(file)
    buffer = io.BytesIO()
    processed_image.save(buffer, format="JPEG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/jpeg")