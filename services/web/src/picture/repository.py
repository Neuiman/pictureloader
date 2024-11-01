from typing import Protocol, Annotated

import httpx
from fastapi import UploadFile, HTTPException
from fastapi.params import Depends
from sqlalchemy import insert, select, update, delete
from src.config import Settings
from src.picture.models import Picture
from src.database import session_maker


class PictureRepositoryProtocol(Protocol):

    async def add_picture(self, data: dict):
        ...

    async def get_all(self):
        ...

    async def get_picture_data_by_id(self, id: int):
        ...

    async def update_picture_data(self, id: int, data: dict):
        ...

    async def delete_picture(self, id: int) -> str:
        ...

    async def send_picture_in_processing_service(self, file: UploadFile):
        ...



class PictureRepositoryImp:

    async def add_picture(self, data: dict) -> int:
        async with session_maker() as session:
            stmt = insert(Picture).values(**data).returning(Picture.id)
            result = await session.execute(stmt)
            await session.commit()

            return result.scalar_one()



    async def get_all(self):
        async with session_maker() as session:
            stmt = select(Picture)
            result = await session.execute(stmt)
            result = [row[0] for row in result.all()]

            return result


    async def get_picture_data_by_id(self, id: int):
        async with session_maker() as session:
            stmt = select(Picture).where(Picture.id == id)
            result = await session.execute(stmt)
            result = [row[0] for row in result.all()]

            return result


    async def update_picture_data(self, id: int, data: dict):
        async with session_maker() as session:
        
            stmt = select(Picture).where(Picture.id == id)
            result = await session.execute(stmt)
            result = [row[0] for row in result.all()][0]
            await session.commit()

            return result

    async def delete_picture(self, id: int) -> str:
        async with session_maker() as session:
            stmt = delete(Picture).where(Picture.id == id)
            await session.execute(stmt)
            await session.commit()

            return "deleted"

    async def send_picture_in_processing_service(self, file: UploadFile):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                Settings.URL_PICTURE_PROCESSOR,
                files={"file": (file.filename, file.file, file.content_type)}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Image processing failed")

            return response.content


async def get_picture_repository() -> PictureRepositoryProtocol:
    return PictureRepositoryImp()

