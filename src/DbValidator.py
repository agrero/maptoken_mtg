from .RequestHandler import RequestHandler

class DbValidator(RequestHandler):

    def __init__(self, base_url:str):
        super().__init__(base_url)

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
        deck_ids = self.get_request('/cards/deck_id/').json()

        # iterate decklist ids
        for deck_id in deck_ids:
            req = self.get_request(f'/cards/deck_id/{deck_id}').json()

            # filter to only degenerate instances
            req = [i for i in req if i in _get_dup_ids_from_request(req)]
            
            for card_id in req:
                # delete based on the ids
                self.delete_request(
                    f'/cards/{card_id}'
                )