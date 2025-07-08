from pyrchidekt.api import getDeckById
from pyrchidekt.deck import Deck

from src.db_models import *

from src.RequestHandler import RequestHandler

from tqdm import tqdm


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
                # post commander and cardlist

                # # commander
                self.add_commander(deck, archidekt_id)
                
                self.add_cards(deck, archidekt_id)

    def get_start(self) -> int:
        req = self.reqhand.get_request('/cards/latest/')
        return req.json()['decklist_id']
                    

    def add_cards(self, deck:Deck, archidekt_id:int) :
        for arch_card in deck.cards:
            reqs = self.reqhand.post_request(
                CardCreate(
                    decklist_id = archidekt_id,
                    count = arch_card.quantity,
                    name = arch_card.card.oracle_card.name
                ).model_dump(), 
                post_url = self.reqhand.url + '/cards/'
            )

    def add_commander(self, deck:Deck, archidekt_id:int):
        # # commander
        self.reqhand.post_request(
            # this will not work for partners
            CommanderCreate(
                name = self._get_commander(deck)[0], 
                decklist_id = archidekt_id
            ).model_dump(), 
            post_url = self.reqhand.url + '/commanders/'
        )

    def _is_commander(self, deck:Deck):
        return deck.format == 3
    
    def _get_commander(self, deck:Deck):
        cards = [i.cards for i in deck.categories 
                if i.name == 'Commander']
        
        cards = [i[0].card.oracle_card.name for i in cards]
        
        
        return cards if len(cards) >= 1 else ['']


if __name__ == '__main__':

    scraper = Scraper(db_url='http://127.0.0.1:8000')


    batch_size = 1000
    start = scraper.get_start()
    print(start)
    stop = start + batch_size

    scraper.scrape(start, stop)
