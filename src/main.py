import json
from pprint import pprint
import base64
import os

from fastapi import FastAPI, HTTPException, Response
from loguru import logger

from models import LabelRequest, ThrowRequest, Throw
import repository_sqlmodel as db

DATA_PATH = "../data"

app = FastAPI()
engine = db.get_engine()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/throws")
async def throw(throw_request: ThrowRequest):
    throw_path = os.path.join(DATA_PATH, throw_request.throw_id)
    save_path = os.path.join(throw_path, f"{throw_request.series_id}.png")

    # create missing directories
    os.makedirs(throw_path, exist_ok=True)

    with open(save_path, 'wb') as f:
        f.write(base64.urlsafe_b64decode(throw_request.img_str))

    throw_entity = Throw.from_request(throw_request)
    db.add_throw(engine, throw_entity)

    return {"message": "success"}

@app.get("/throws/{throw_id}/{series_id}/img")
async def get_throw_img(throw_id: str, series_id: int):
    """
    Loads an image as bytes.
    """
    image_path = os.path.join(DATA_PATH, throw_id, f"{series_id}.png")

    try:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
            headers = { 'Access-Control-Allow-Origin': '*' }
            return Response(content=image_bytes, media_type="image/png", headers=headers)
    except FileNotFoundError:
        raise HTTPException(404, "Image not found")

@app.get("/throws/list")
async def get_throw_ids():
    return db.get_throw_ids(engine)

@app.get("/labels/{throw_id}/{series_id}")
async def get_label(throw_id: str, series_id: int):
    throw = db.get_throw(engine, throw_id, series_id)

    if throw is None:
        raise HTTPException(404, "Throw not found")
    if throw.label is None or len(throw.label) == 0:
        raise HTTPException(404, "Label not set")
    logger.debug("label str", throw.label)
    label = json.loads(throw.label)
    return label

@app.get("/labels")
async def get_all_labels():
    pass

@app.put("/labels/{throw_id}/{series_id}")
async def update_label(throw_id: str, series_id: int, label: LabelRequest):
    db.update_throw_label(engine, throw_id, series_id, label)
    return {"message": "success"}