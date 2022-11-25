from pathlib import Path
import json
import dbm

from models import ThrowSequenceRequestModel, ThrowSequenceLabelsRequestModel

DB_FILENAME = "database.dbm"
DB_PATH = Path() / ".." / "db" / DB_FILENAME

db = None


def start():
    global db
    if not DB_PATH.exists():
        db = dbm.open(DB_PATH.as_posix(), "n")
        db.close()
    db = dbm.open(DB_PATH.as_posix(), "w")

def add_throw_sequence(throw_sequence: ThrowSequenceRequestModel):
    throw_dicts = []
    for throw in throw_sequence.throws:
        throw_dict = throw.__dict__
        del throw_dict['imageString']
        throw_dicts.append(throw_dict)
    throw_sequence_dict = {
        'id': throw_sequence.id,
        'creationDate': throw_sequence.creationDate.isoformat(),
        'throws': throw_dicts
    }

    db[throw_sequence.id] = json.dumps(throw_sequence_dict, default=lambda o: o.__dict__)

def get(throw_sequence_id: str):
    if not str.encode(throw_sequence_id) in db.keys():
        return None
    return db[throw_sequence_id]

def get_all():
    return [db[key] for key in db.keys()]

def get_ids():
    return db.keys()

def delete_throw_sequence(throw_sequence_id: str):
    if not throw_sequence_exists(throw_sequence_id):
        return False
    del db[throw_sequence_id]
    return True

def throw_sequence_exists(throw_sequence_id: str):
    return throw_sequence_id in db

def update_label(throw_sequence_id: str, throw_sequence_labels: ThrowSequenceLabelsRequestModel):
    throw_sequence = json.loads(db[throw_sequence_id])
    
    updated_throws = []
    for throw in throw_sequence['throws']:
        id_ = throw['id']
        updated_label = throw['imageLabel']
        if id_ == 0:
            updated_label = throw_sequence_labels.throw_1_label
        elif id_ == 1:
            updated_label = throw_sequence_labels.throw_2_label
        elif id_ == 2:
            updated_label = throw_sequence_labels.throw_3_label
        else:
            raise ValueError(f'Unknown ThrowSequence ThrowId {id_}')
        updated_throws.append({**throw, 'imageLabel': updated_label})
    throw_sequence['throws'] = updated_throws
    db[throw_sequence_id] = json.dumps(throw_sequence, default=lambda o: o.__dict__)

def shutdown():
    db.close()
