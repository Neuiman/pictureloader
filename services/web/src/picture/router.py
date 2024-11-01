import io

import aiofiles
import httpx
from PIL import Image
from fastapi import APIRouter, UploadFile, File
import shutil

from fastapi.params import Depends
from fastapi.exceptions import HTTPException
from src.auth.utils import get_current_user
from src.picture.schemas import PictureSchemaAdd, PictureNameSchema
from src.picture.service import PictureService

router = APIRouter()

@router.post("/upload")
async def add_new_picture(picture_service: PictureService,
                          current_user = Depends(get_current_user),
                          upload_file: UploadFile = File()):

    picture = await picture_service.get_new_picture_data(upload_file)

    if type(picture) is dict:
        return picture


    picture_id = await picture_service.add_picture(picture)

    return picture_id


@router.get("/get_all")
async def get_all_info_pictures(picture_service: PictureService, current_user = Depends(get_current_user)):
    picture_dict = await picture_service.get_all_pictures()
    return picture_dict


@router.get("/get_by_id")
async def get_picture_info_by_id(id: int, picture_service: PictureService, current_user = Depends(get_current_user)):
    picture = await picture_service.get_picture_by_id(id)
    return picture


@router.patch("/update_by_id")
async def update_picture_data(id: int, picture: PictureNameSchema, picture_service: PictureService,
                              current_user = Depends(get_current_user)):
    updated_picture = await picture_service.update_picture_name_by_id(id, picture=picture)
    return updated_picture


@router.delete("/delete_by_id")
async def delete_picture_by_id(id: int, picture_service: PictureService, current_user = Depends(get_current_user)):
    delete_request = await picture_service.delete_picture_by_id(id=id)
    return delete_request
