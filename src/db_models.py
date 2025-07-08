from sqlmodel import Field, SQLModel

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
