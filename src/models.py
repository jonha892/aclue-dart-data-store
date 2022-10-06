import logging
from multiprocessing.sharedctypes import SynchronizedString
from typing import List
import json
from datetime import datetime
import json

from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field, SQLModel, JSON


###
### API
###

class CatVecRequestModel(BaseModel):
    x: int
    y: int

class ImageLabelRequestModel(BaseModel):
    planeCoordinates: List[CatVecRequestModel]
    dartCoordinates: List[CatVecRequestModel]


class ThrowRequestModel(BaseModel):
    id: int
    scoreString: str
    imageResolution: CatVecRequestModel
    imageLabel: ImageLabelRequestModel
    imageString: str

class ThrowSequenceRequestModel(BaseModel):
    id: str
    creationDate: datetime
    throws: List[ThrowRequestModel]


###
### Database
###

class ThrowSequence(SQLModel, table=True):
    id: str = Field(primary_key=True)
    creationDate: datetime = Field(nullable=False)
    throws: List[str] = Field(sa_column=Column(JSON), nullable=False)

    class Config:
        arbitrary_types_allowed = True
    
    @staticmethod
    def from_request(throw_sequence_request: ThrowSequenceRequestModel):

        uvicorn_info_logger = logging.getLogger("uvicorn.info")
        
        throws = []
        for t in throw_sequence_request.throws:
            throw_dict = t.dict()
            del throw_dict['imageString'] # don't save image in database
            throw_dict_str = json.dumps(throw_dict)
            throws.append(throw_dict_str)

        uvicorn_info_logger.info(f"throws: {json.dumps(throws)}")

        return ThrowSequence(
            id=throw_sequence_request.id,
            creationDate=throw_sequence_request.creationDate,
            throws=throws)