import json
from pprint import pprint
import base64
import os
import logging

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models import ThrowSequence, ThrowSequenceRequestModel

import repository_sqlmodel as repo

logger = logging.getLogger("api")
DATA_PATH = "../data"
engine = repo.get_engine()

app = FastAPI(debug=True)

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/throw-sequences/{throwSequenceId}")
async def postNewThrowSequence(request: ThrowSequenceRequestModel):
    throw_sequence_path = os.path.join(DATA_PATH, request.id)
    # create missing directories
    os.makedirs(throw_sequence_path, exist_ok=True)
    
    for throw in request.throws:
        throw_path = os.path.join(throw_sequence_path, str(throw.id) + '.png')
        with open(throw_path, 'wb') as f:
            f.write(base64.urlsafe_b64decode(throw.imageString))

    throw_sequence_entity = ThrowSequence.from_request(request)
    repo.add_throw_sequence(engine, throw_sequence_entity)

    return {}

@app.delete("/api/throw-sequences/{throwSequenceId}")
async def deleteThrowSequence(throwSequenceId):
    deleted = repo.delete_throw_sequence(engine, throwSequenceId)
    return { "deleted": deleted}


@app.get("/api/labels")
async def getLalbelOverview():
    all_throw_sequences = repo.get_all(engine)

    res = []
    for sequence in all_throw_sequences:
        throws = list(map(lambda x: json.loads(x), sequence.throws))

        is_fully_labeled = all(map(lambda t: \
            len(t['imageLabel']['planeCoordinates']) > 0 and \
            len(t['imageLabel']['dartCoordinates']) > 0
            , throws))
        
        res.append({
            'throwSequenceId': sequence.id,
            'creationDate': sequence.creationDate,
            'isFullyLabeled': is_fully_labeled,
        })

    return res

@app.get("/test")
async def test():
    r = repo.get_all(engine)
    return r

"""
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

    #Loads an image as bytes.

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
"""
