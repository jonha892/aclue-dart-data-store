import json
import base64
import os
import logging
from pathlib import Path
import shutil

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import ThrowSequenceLabelsRequestModel, ThrowSequenceRequestModel
import repository_dbm as repo

logger = logging.getLogger("api")
DATA_PATH = Path() / '..' / 'data'

repo.start()

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

@app.on_event("shutdown")
def shutdown_event():
    repo.shutdown()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/throw-sequences/{throwSequenceId}")
async def postNewThrowSequence(request: ThrowSequenceRequestModel, throwSequenceId: str):
    throw_sequence_path = DATA_PATH / throwSequenceId
    # create missing directories
    os.makedirs(throw_sequence_path, exist_ok=True)
    
    for throw in request.throws:
        throw_path = throw_sequence_path / (str(throw.id) + '.png')
        with open(throw_path.as_posix(), 'wb') as f:
            f.write(base64.urlsafe_b64decode(throw.imageString))

    repo.add_throw_sequence(request)

    return {}

@app.get("/api/throw-sequences/{throwSequenceId}")
async def getThrowSequence(throwSequenceId: str):
    throw_sequcnce = repo.get(throwSequenceId)

    print(throw_sequcnce)
    if not throw_sequcnce:
        raise HTTPException(status_code=404, detail="ThrowSequence not found") 
    
    throw_sequence = json.loads(throw_sequcnce)
    throws_with_image = []
    for throw in throw_sequence['throws']:
        throw_image_path = DATA_PATH / throwSequenceId / (str(throw['id']) + '.png')
        with open(throw_image_path, 'rb') as f:
            base_64_image = base64.b64encode(f.read())
            throws_with_image.append({**throw, 'imageString': base_64_image})
    throw_sequence['throws'] = throws_with_image
    return throw_sequence

@app.delete("/api/throw-sequences/{throwSequenceId}")
async def deleteThrowSequence(throwSequenceId: str):
    
    db_deleted = repo.delete_throw_sequence(throwSequenceId)

    throw_sequence_path = DATA_PATH / throwSequenceId
    file_deleted = False
    
    if throw_sequence_path.is_dir():
        file_deleted = True
        shutil.rmtree(throw_sequence_path)

    return { "db_deleted": db_deleted, "file_deleted": file_deleted }


@app.get("/api/labels")
async def getLabelOverview():
    throw_sequences = [json.loads(t) for t in repo.get_all()]
    label_overview = [ {'throwSequenceId': t['id'], 'creationDate': t['creationDate'], 'isFullyLabeled': is_fully_labeled(t)} for t in throw_sequences]

    return label_overview

@app.post("/api/labels/{throwSequenceId}") 
async def postThrowSequenceLabels(thowSequenceLabels: ThrowSequenceLabelsRequestModel, throwSequenceId: str):
    if not repo.throw_sequence_exists(throwSequenceId):
        raise HTTPException(status_code=404, detail="ThrowSequence not found") 

    repo.update_label(throwSequenceId, thowSequenceLabels)
    return {}

@app.get("/test")
async def test():
    r = repo.get_all()
    return r

@app.get("/api/ids")
async def getIds():
    r = repo.get_ids()
    return r


def is_fully_labeled(throw_sequence_dict):
    return all(map(lambda throw: \
            len(throw['imageLabel']['planeCoordinates']) > 0 and \
            len(throw['imageLabel']['dartCoordinates']) > 0
            , throw_sequence_dict["throws"]))