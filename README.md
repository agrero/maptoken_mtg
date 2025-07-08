# Read Me
## Installation

## Running

### 1. Starting the Database

In your first terminal type:

```bash 
fastapi dev database.py # for development mode

# or

fastapi database.py # or whatever it is for non dev mode
```

### 1.1 Database Documentation

Type Into Your Browser Window: [https://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

If it stalls make sure your database is running in the terminal.

### 2. Running the Scraper

In a seperate terminal that is currently running your database.

```bash
python scraper.py
```
This should base its starting position off of whatever the latest decklist_id is in your database

## To Do

### 1. Query Decklists as UMAP precursors

1. Query
2. Receive Response
3. Convert to Correct <b>Shape</b>

The following is the correct <b>Shape</b>

|decklist_id|cardname_n|cardname_n+1|
|-----------|----------|------------|
|decklist i |#n in i   |#n+1 in i   |
|decklist i+1|#n in i+1|#n+1 in i+1 |

### 2. Label Ids as good or bad and commander or not

### 3. Cleanup the Riff Raff

I haven't really checked but not all of these decks are valid so I propose 2 methodologies

1. If its close to being legal (in terms of card count)
    - If its above remove basic lands or cards at random
    - If its below add a basic land until you reach 100

2. Label all the ones that aren't close as bad links in the above list you'll make
    - This'll include decks that have no commander of which we just list with '' for the commander name