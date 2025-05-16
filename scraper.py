

from pyrchidekt.api import getDeckById
from pyrchidekt.deck import Deck

import pandas as pd


# will need a way to screen good links from bad
# also need a way to save

deck = getDeckById(40)

def scrape_categories(deck:Deck):
    
    categories = [[i.card.oracle_card.id for i in deck.categories[j].cards]
                  for j in range(len(deck.categories))]
    
    category_names = [i.name for i in deck.categories]
    categories = {
        category_names[ndx]:category 
        for ndx, category in enumerate(categories)
    }

    return categories

# for iterating

# precompile a list of all of the names and initialize the categories
# with empty dictionaries to lists

# iterate through categories and extend lists 


cats = scrape_categories(deck)
print(cats)

# print(deck.categories[1].name)
# print([[i.card.oracle_card.id for i in deck.categories[j].cards]
#        for j in range(len(deck.categories))])



# for category in deck.categories:
#     print(f'{category.name}')
#     for card in category.cards:
#         print(f'\t{card.quantity} {card.card.oracle_card.name}')
        
#     print('')

no_decks = 10
deck_ids = [i for i in range(10)]

# to extract name

# deck.cards.id

# bingo
# print(deck.cards[0].card.id)

# categories

# 



