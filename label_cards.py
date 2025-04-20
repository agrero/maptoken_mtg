import pandas as pd
import os



def manual_label_cards(decklist, label):
    """iterate through the decklist 
    and manually apply a label"""
    labels = []
    for i in decklist.index:
        row = decklist.iloc[i,:]
        print(row['name'])
        print(row['type_line'])
        print(row['oracle_text'])
        inp = input(f'Label: ')
        print('\n')
        labels.append(inp)
    
    decklist[label] = labels

    return decklist


decklist = pd.read_csv(os.path.join('data', 'decklist.csv'))
new_label = 'newlabel'

manual_label_cards(decklist, new_label)



print(decklist)