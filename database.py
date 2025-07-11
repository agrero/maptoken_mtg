from typing import Annotated

from fastapi import Depends, FastAPI, Query, HTTPException
from sqlmodel import Session, SQLModel, create_engine, select

from src.db_models import *

import os

database_path = os.path.join('data','database.db')

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{database_path}"

connect_args = {"check_same_thread": False}
db_engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(db_engine)

def get_session():
    with Session(db_engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/commanders/", response_model=CommanderPublic)
def create_commander(commander : CommanderCreate, session: SessionDep):
    db_commander = Commander.model_validate(commander)
    session.add(db_commander)
    session.commit()
    session.refresh(db_commander)
    return db_commander

@app.post("/cards/", response_model=CardPublic)
def create_card(card: CardCreate, session: SessionDep):
    db_card = Card.model_validate(card)
    session.add(db_card)
    session.commit()
    session.refresh(db_card)
    return db_card

@app.get('/cards/{offset}/{limit}/', response_model=list[CardPublic])
def get_cards(
    session:SessionDep,
    offset:int = 0,
    limit:int = 100
):
    cards = session.exec(select(Card).offset(offset).limit(limit)).all()
    return cards

@app.get("/cards/", response_model=list[CardPublic])
def read_cards(
    session: SessionDep,
    offset: int = 0,
    lim:int = 100
):
    cards = session.exec(select(Card).offset(offset).limit(lim)).all()
    return cards

@app.get('/cards/deck_id/{id}', response_model=list[CardPublic])
def get_deck_by_id(session:SessionDep, id:int):
    return session.exec(
        select(Card).where(Card.decklist_id == id)
    )

@app.get('/cards/deck_id/', response_model=list[int])
def get_deck_ids(session:SessionDep):
    
    cards = session.exec(select(Card)).all()

    return list({i.decklist_id for i in cards})

# i think this should be middleware
@app.get("/cards/latest/", response_model=CardPublic)
def get_last_card(session: SessionDep, offset:int=0):
    return session.exec(select(Card).offset(offset)).all()[-1]

@app.delete("/cards/{card_id}")
def delete_card(card_id: int, session: SessionDep):
    card = session.get(Card, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    session.delete(card)
    session.commit()
    return {"ok": True}

# i think this just makes everything so heckin slow
# @app.post('/data/training/', response_model=TrainingData)
# def post_training_data(session: SessionDep, data : TrainingBase):

#     training_data = TrainingData.model_validate(data)

#     session.add(training_data)
#     session.commit()
#     session.refresh(training_data)

#     return training_data

# @app.get("/cards/{card_id}", response_model=CardPublic)
# def read_card(card_id: int, session: SessionDep):
#     card = session.get(Card, card_id)
#     if not card:
#         raise HTTPException(status_code=404, detail="Card not found")
#     return card


# @app.patch("/cards/{card_id}", response_model=CardPublic)
# def update_card(card_id: int, card: CardUpdate, session: SessionDep):
#     card_db = session.get(Card, card_id)
#     if not card_db:
#         raise HTTPException(status_code=404, detail="Card not found")
#     card_data = card.model_dump(exclude_unset=True)
#     card_db.sqlmodel_update(card_data)
#     session.add(card_db)
#     session.commit()
#     session.refresh(card_db)
#     return card_db


