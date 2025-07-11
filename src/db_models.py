from sqlmodel import Field, SQLModel

# kinda makes it hard to find what this is obfuscating
from .helper import *

# COMMANDERS

class CommanderBase(SQLModel):
    name : str = Field(index=False)
    decklist_id : int | None = Field(default=None, index=True)

class Commander(CommanderBase, table = True):
    id : int | None = Field(default=None, primary_key=True)

class CommanderPublic(CommanderBase):
    pass

class CommanderCreate(CommanderBase):
    pass

# CARDS

class CardBase(SQLModel):
    decklist_id : int | None = Field(default=None, index=True)
    count: int | None = Field(default=0, index=False)
    name: str = Field(index=False)

class Card(CardBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class CardPublic(CardBase):
    id: int

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    name: str | None = None
    age: int | None = None

# TRAINING DATA # this is kinda bad ngl

# class TrainingBase(create_TrainingData()):
#     """Base Training Data Class as constured in the <b>helper</b> module"""
#     pass

# class TrainingData(TrainingBase, table=True):
#     id: int = Field(default=None, primary_key=True)
