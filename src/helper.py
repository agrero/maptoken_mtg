import pandas as pd

import os

from sqlmodel import Field, SQLModel
from pydantic import create_model
from typing import Union

def cache(to_cache:pd.DataFrame, cache_name:str, cache_dir:str) -> None:
    to_cache.to_parquet(
        os.path.join(cache_dir, cache_name)
    )

def cache_cardnames(cardname_source:str) -> None:
    """cache cardnames as a parquet file"""

    cards = pd.read_json(
        os.path.join('data', cardname_source)
    )

    cards = cards.loc[:,['name']].drop_duplicates()
    
    cards.to_parquet(
        os.path.join('data', 'cache', 'cardname_cache.parquet')
    )

def create_TrainingData() -> SQLModel:
    """will eventually need to decide to read from cache or not"""
    def _fill_cards(cards:pd.DataFrame):
        return {
            i[1]: (Union[int, None], Field(description=str(i[1])))
            for i in [(j, cards.iloc[j,0]) for j in cards.index.tolist()]
        }
    
    # need to fix cardnames here

    cards = fix_cached_cardnames(pd.read_parquet(
        os.path.join('data', 'cache', 'cardname_cache.parquet')
    ))

    return create_model('TrainingData',
        __base__ = SQLModel,
        decklist_id=(Union[int, None], Field(description='Archidekt Decklist ID')),
        # fill card names as kwargs
        **_fill_cards(cards)
    )


def fix_cached_cardnames(cards) -> None:

    """Read in the cardname cache and clean it up"""

    def _clean_underscores(cards):
        problem_ndxs = [ndx for ndx, i 
                        in enumerate(cards.loc[: , 'name'].tolist())
                        if i[0] == '_']
    
        fixed_names = [f' {cards.iloc[i,0]}' for i in problem_ndxs]

        return problem_ndxs, fixed_names

    ndxs, names = _clean_underscores(cards)

    for ndx, i in enumerate(ndxs):
        cards.iloc[i,0] = names[ndx]
   
    return cards
    # cards.to_parquet(cache_path)

    