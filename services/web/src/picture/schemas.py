from datetime import datetime

from pydantic import BaseModel

class PictureNameSchema(BaseModel):
    name: str
    
    
class PictureSchema(BaseModel):
    id: int
    name: str
    path: str
    load_date: datetime
    resolution: str
    size: float


    class Config:
        from_attributes = True


class PictureSchemaAdd(BaseModel):
    name: str
    path: str
    resolution: str
    size: float