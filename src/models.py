from typing import List
from datetime import datetime

from pydantic import BaseModel

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


class ThrowSequenceLabelsRequestModel(BaseModel):
    throw_1_label: ImageLabelRequestModel
    throw_2_label: ImageLabelRequestModel
    throw_3_label: ImageLabelRequestModel