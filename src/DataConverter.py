import pandas as pd
import os

from . import helper

from .RequestHandler import RequestHandler

class _DataConverter(RequestHandler):
    def __init__(self, base_url:str):
        super().__init__(base_url)

    def _card_request_to_pandas(self, 
                                get_req:dict, 
                                card_names:pd.DataFrame
                                ) -> pd.DataFrame:
            
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
    
    def _make_umap_zeroes(self, card_names:list[str]) -> pd.DataFrame:
        return pd.DataFrame(
            data=[[0 for i in range(len(card_names))]],
            columns=card_names,
            index=[0]
        ).astype(pd.Int8Dtype())

    def _delete_temp_cached_files(self, cache_dir:str) -> None:
        rm_list = [fname for fname in os.listdir(cache_dir) 
                    if 'data_' in fname]
        for path in [os.path.join(cache_dir, i) for i in rm_list]:
            os.remove(path)

class DataConverter(_DataConverter):
    """Class responsible for converting queryed data into a useable format"""
    def __init__(self, base_url:str):
        super().__init__(base_url)

    def card_to_label(self, cache=False, offset:int=0, batch_size=100):

        if cache:
            card_names = helper.cache_cardnames('oracle-cards-20250414210533.json')

        card_names = pd.read_parquet(
            os.path.join('data', 'cache', 'cardname_cache.parquet')
        )

        return self._card_request_to_pandas(
            self.get_request(f'/cards/{offset}/{batch_size}/').json(), 
            card_names # awk here
        )    
    def iter_cache_data(self, no_iterations:int, batch_size:int) -> None:
        
        cache_dir = os.path.join('data', 'cache')

        for i in range(no_iterations):

            data = self.card_to_label(
                cache=False, offset=i*batch_size, batch_size=batch_size
            ).sort_index(axis=0)
            
            first_id, last_id = data.index[0], data.index[-1]

            helper.cache(
                data, f'data_{first_id}_{last_id}.parquet', cache_dir
            )
        
        cache_dir_list = [i for i in os.listdir(cache_dir) if 'data' in i]

        # # empty dataframe

        card_names = pd.read_parquet(
                os.path.join(cache_dir,'cardname_cache.parquet')
        ).name.tolist() 
        
        data = self._make_umap_zeroes(card_names)

        for path in cache_dir_list:
            path = os.path.join(cache_dir, path)
            data = pd.concat([data, pd.read_parquet(path)])

        helper.cache(data, 'training.parquet', cache_dir)
        self._delete_temp_cached_files(cache_dir)