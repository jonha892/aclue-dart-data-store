from typing import List
import json

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


###
### API
###
class ThrowRequest(BaseModel):
    throw_id: str
    series_id: str
    img_str: str
    dart: str


class RelativePosition(BaseModel):
    x: float
    y: float

class LabelRequest(BaseModel):
    anchor_top: RelativePosition
    anchor_bottom: RelativePosition
    anchor_left: RelativePosition
    anchor_right: RelativePosition

    darts: List[RelativePosition]


###
### Database
###
class Throw(SQLModel, table=True):
    throw_id: str = Field(primary_key=True)
    series_id: int = Field(primary_key=True)
    dart: str # maybe list of stirngs?
    label: str

    @staticmethod
    def from_request(throw_request: ThrowRequest):
        return Throw(throw_id=throw_request.throw_id,
                        series_id=throw_request.series_id,
                        dart=throw_request.dart,
                        label=json.dumps({}))