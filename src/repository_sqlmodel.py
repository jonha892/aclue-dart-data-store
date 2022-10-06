
import os
import json

from sqlmodel import SQLModel, Session, create_engine, engine, select
import logging

logger = logging.getLogger("api")

from models import ThrowRequestModel, ThrowSequence, ThrowSequenceRequestModel

DB_PATH = "../db"
DB_FILENAME = "database_2.sqlite3"
DB_URL = f"sqlite:///{os.path.join(DB_PATH, DB_FILENAME)}"

def create_database_dir(db_path: str):
    print("creating db path", db_path)
    os.makedirs(db_path, exist_ok=True)


def create_database():
    create_database_dir(DB_PATH)
    engine = create_engine(DB_URL, echo=True)
    SQLModel.metadata.create_all(engine)

def get_engine():
    logger.info("test")
    return create_engine(DB_URL, echo=True)


def add_throw_sequence(engine, throw: ThrowSequence):
    with Session(engine) as session:
        session.add(throw)
        session.commit()

def delete_throw_sequence(engine, throw_sequence_id: str):
    r = False
    with Session(engine) as session:
        statement = select(ThrowSequence).where(ThrowSequence.id == throw_sequence_id)
        results = session.exec(statement)
        
        throw_sequence = results.one_or_none()
        print("Throw_sequence: ", throw_sequence)

        if throw_sequence:
            r = True
            session.delete(throw_sequence)
            session.commit()
    return r

def get_all(engine):
    with Session(engine) as session:
        statement = select(ThrowSequence)
        results = session.exec(statement)
        res = []
        for r in results:
            res.append(r)
        return res
"""
def add_throw(engine, throw: ThrowRequestModel):
    with Session(engine) as session:
        session.add(throw)
        session.commit()

def update_throw_label(engine: engine, throw_id: str, series_id: str, label_request: LabelRequest):
    with Session(engine) as session:
        existing_throw = session.get(ThrowRequestModel, (throw_id, series_id))
        if existing_throw is None:
            return False
            
        print(f"Found existing throw: {existing_throw}" )
        log.debug(f"Found existing throw: {existing_throw}")
        #logger.debug(f"Found existing throw: {existing_throw.__repr__}", feature="f-strings" )
        logger.debug(f"Test{ {'a': 1}}", feature="f-strings" )
        logger.debug(f"Test2 ", {'a': 2} )

        label_string = json.dumps(label_request, default=lambda x: x.__dict__)
        existing_throw.label = label_string
        session.add(existing_throw)
        session.commit()

def get_throw(engine: engine, throw_id: str, series_id: int):
    with Session(engine) as session:
        entity = session.get(ThrowRequestModel, (throw_id, series_id))
        return entity

def get_throw_ids(engine: engine):
    with Session(engine) as session:
        statement = select(ThrowRequestModel.throw_id, ThrowRequestModel.series_id)
        results = session.execute(statement)
        r = results.all()
        return r
"""

if __name__ == "__main__":
    logger.debug("setting up the database..")
    create_database()