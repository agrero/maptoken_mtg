from pyrchidekt.api import getDeckById
from pyrchidekt.deck import Deck

from src.db_models import *

from src.RequestHandler import RequestHandler

from src import helper

from tqdm import tqdm

import os

import pandas as pd


class Scraper:
    
    def __init__(self, db_url:str):
        self.reqhand = RequestHandler(db_url)

    def scrape(self, start:int, stop:int):
        for archidekt_id in tqdm(range(start, stop)):
            try:
                deck = getDeckById(archidekt_id)
            except:
                continue
            if self._is_commander(deck):
                self.add_commander(deck, archidekt_id)
                self.add_cards(deck, archidekt_id)

    def get_start(self) -> int:
        req = self.reqhand.get_request('/cards/latest/')
        return req.json()['decklist_id']             

    def add_cards(self, deck:Deck, archidekt_id:int) :
        for arch_card in deck.cards:
            self.reqhand.post_request(
                CardCreate(
                    decklist_id = archidekt_id,
                    count = arch_card.quantity,
                    name = arch_card.card.oracle_card.name
                ).model_dump(), 
                post_url = self.reqhand.url + '/cards/'
            )

    def add_commander(self, deck:Deck, archidekt_id:int):
        # # commander

        commander_name = self._get_commander(deck)
        
        self.reqhand.post_request(
            # this will not work for partners
            CommanderCreate(
                name = commander_name, 
                decklist_id = archidekt_id
            ).model_dump(), 
            post_url = self.reqhand.url + '/commanders/'
        )

    def _query_cards(self, get_url:str='/cards/'):
        req = self.reqhand.get_request(get_url)
        return [i for i in req.json()]

    def _is_commander(self, deck:Deck):
        return deck.format == 3
    
    def _get_commander(self, deck:Deck):
        cards = [i.cards for i in deck.categories 
        if i.name == 'Commander']
        try:
            cards = [i[0].card.oracle_card.name for i in cards]
            return '+'.join(cards)
        except:
            return ''

    def _make_umap_zeroes(self, card_names:list[str]) -> pd.DataFrame:
        return pd.DataFrame(
            data=[[0 for i in range(len(card_names))]],
            columns=card_names,
            index=[0]
        ).astype(pd.Int8Dtype())


    def _iter_cache_data(self, no_iterations:int, batch_size:int) -> None:
        
        def __delete_temp_cached_files(cache_dir:str) -> None:
            rm_list = [fname for fname in os.listdir(cache_dir) 
                       if 'data_' in fname]
            for path in [os.path.join(cache_dir, i) for i in rm_list]:
                os.remove(path)

        cache_dir = os.path.join('data', 'cache')

        for i in range(no_iterations):

            data = scraper.card_to_label(
                cache=False, offset=i*batch_size, batch_size=batch_size
            ).sort_index(axis=0)
            
            first_id, last_id = data.index[0], data.index[-1]

            cache(
                data, f'data_{first_id}_{last_id}.parquet', cache_dir
            )
        
        cache_dir_list = [i for i in os.listdir(cache_dir) if 'data' in i]

        # # empty dataframe

        card_names = pd.read_parquet(
                os.path.join(cache_dir,'cardname_cache.parquet')
        ).name.tolist() 
        
        data = scraper._make_umap_zeroes(card_names)

        for path in cache_dir_list:
            path = os.path.join(cache_dir, path)
            data = pd.concat([data, pd.read_parquet(path)])

        cache(data, 'training.parquet', cache_dir)
        __delete_temp_cached_files(cache_dir)

    def card_to_label(self, cache=False, offset:int=0, batch_size=100):

        def _get_req_to_pandas(get_req:dict, card_names:pd.DataFrame) -> pd.DataFrame:
            
            # get a set of the current decklist ids
            decklist_ids = list({i['decklist_id'] for i in get_req})

            data = pd.DataFrame(
                data=[[0 for i in range(card_names.shape[0])] 
                      for j in decklist_ids],
                columns=card_names.name.tolist(),
                index=decklist_ids
            )

            for card in get_req:
                data.loc[card['decklist_id'], card['name']] = card['count']

            return data.astype(pd.Int8Dtype())

        if cache:
            card_names = helper.cache_cardnames('oracle-cards-20250414210533.json')

        card_names = pd.read_parquet(
            os.path.join('data', 'cache', 'cardname_cache.parquet')
        )

        return _get_req_to_pandas(
            scraper.reqhand.get_request(f'/cards/{offset}/{batch_size}/').json(), 
            card_names # awk here
        )
    
    def remove_duplicate_cards(self) -> None:
        # in the future we can make this get specific decks 
        # then have some iterable it can iterate through to remove shit
        def _get_dup_ids_from_request(req:list[dict]) -> list[int]:
            
            dup_ids = [i['name'] for i in req]

            dup_ids = [dup_ids.count(j) for j in dup_ids]
            dup_ids = [
                i for i in range(len(req)) 
                if i not in 
                [ndx for ndx, i in enumerate(dup_ids) if i > 1]
            ]
            return dup_ids

        # get a list of all decklist ids
        deck_ids = self.reqhand.get_request('/cards/deck_id/').json()

        # iterate decklist ids
        for deck_id in deck_ids:
            req = self.reqhand.get_request(f'/cards/deck_id/{deck_id}').json()

            # filter to only degenerate instances
            req = [i for i in req if i in _get_dup_ids_from_request(req)]
            
            for card_id in req:

                # delete based on the ids
                self.reqhand.delete_request(
                    f'/cards/{card_id}'
                )
    

if __name__ == '__main__':

    scraper = Scraper(db_url='http://0.0.0.0:8000')

    scraper.remove_duplicate_cards()

