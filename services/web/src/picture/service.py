import io
import json
import os
from pathlib import Path

import aiofiles
from PIL import Image
from aiokafka import AIOKafkaProducer
from fastapi import Depends, UploadFile
from typing import Self, Any

from src.kafka import producer
from src.kafka.producer import get_producer
from src.picture.schemas import PictureSchemaAdd, PictureSchema
from src.picture.repository import PictureRepositoryProtocol, get_picture_repository
from typing import Annotated, Protocol


class PictureServiceProtocol(Protocol):
    async def add_picture(self: Self, picture: PictureSchemaAdd):
        ...

    async def get_all_pictures(self: Self):
        ...

    async def get_picture_by_id(self: Self, id: int):
        ...

    async def update_picture_by_id(self: Self, id: int, picture: PictureSchemaAdd):
        ...

    async def delete_picture_by_id(self: Self, id: int):
        ...

    async def get_new_picture_data(self, file: UploadFile) -> PictureSchemaAdd:
        ...

class PictureServiceImp:
    def __init__(self: Self, picture_repository: PictureRepositoryProtocol, producer: AIOKafkaProducer):
        self.picture_repository = picture_repository
        self.producer = producer

    async def add_picture(self: Self, picture: PictureSchemaAdd):
        picture_dict = picture.model_dump()
        picture_id = await self.picture_repository.add_picture(data=picture_dict)
        log = {'event': 'upload', 'uploaded_data': picture_dict}

        serialized_object = json.dumps(log).encode('utf-8')
        await self.producer.send(value=serialized_object)

        return picture_id

    async def get_all_pictures(self: Self):
        all_picture_data = await self.picture_repository.get_all()
        return all_picture_data

    async def get_picture_by_id(self: Self, id: int):
        picture_by_id = await self.picture_repository.get_picture_data_by_id(id)
        return picture_by_id

    async def update_picture_name_by_id(self: Self, id: int, picture: PictureSchemaAdd):
        print(picture)
        picture_dict = picture.model_dump()
        last_picture_data = await self.picture_repository.get_picture_data_by_id(id)
        if not last_picture_data:
            return {"Error": "picture with your ID is not exist"}
        last_picture_data = last_picture_data[0]
        last_name = last_picture_data.name
        log = {"event": "update name", 'last name': last_name, 'current name': picture_dict}
        serialized_object = json.dumps(log).encode('utf-8')
        await self.producer.send(value=serialized_object)

        updated_picture = await self.picture_repository.update_picture_data(id, picture_dict)
        return updated_picture


    async def delete_picture_by_id(self: Self, id: int):
        deleting_picture = await self.picture_repository.get_picture_data_by_id(id)

        if not deleting_picture:
            return {"error": "picture with your ID is not exist"}
        deleting_picture = deleting_picture[0]
        if not os.path.exists(deleting_picture.path):
            return {"error": "picture file does not exist"}
        delete_string = await self.picture_repository.delete_picture(id)

        os.remove(deleting_picture.path)

        log = {'event': "delete", "id": id}
        serialized_object = json.dumps(log).encode('utf-8')

        await self.producer.send(value=serialized_object)
        return delete_string


    async def get_new_picture_data(self, file: UploadFile) -> PictureSchemaAdd | dict:

        content = await self.picture_repository.send_picture_in_processing_service(file)
        image = Image.open(io.BytesIO(content))
        width, height = image.size
        file_size = len(content)
        picture_name = file.filename
        path = f'src/media/{picture_name}'
        filepath = Path(path)
        if filepath.exists():
            return {"error": "a file with the given name exists "}
        async with aiofiles.open(path, 'wb') as file:
            await file.write(content)

        return PictureSchemaAdd(name=picture_name, path=path, size=file_size, resolution=f"{width}x{height}")


async def get_picture_service(repository: PictureRepositoryProtocol = Depends(get_picture_repository),
                              producer: AIOKafkaProducer = Depends(get_producer)) -> PictureServiceProtocol:
    return PictureServiceImp(repository, producer)

PictureService = Annotated[PictureServiceProtocol, Depends(get_picture_service)]


