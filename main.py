from src.DataConverter import DataConverter
from src.DbValidator import DbValidator
from src.Scraper import Scraper


class Main:

    def __init__(
            self, scraper:Scraper, 
            data_converter:DataConverter, 
            db_validator:DbValidator
        ):
        
        self.scraper = scraper
        self.data_converter = data_converter
        self.db_validator = db_validator
    
    def run(self):
        # we can just put whatever we want here
        # this is just a placeholder to make sure it all works
        # really gotta add testing lazy bum
        self.data_converter.iter_cache_data(2, 100)
        pass 


if __name__ == '__main__':

    base_url = 'http://0.0.0.0:8000'
    
    
    main = Main(
        scraper=Scraper(base_url),
        data_converter=DataConverter(base_url),
        db_validator=DbValidator(base_url)
    )

    main.run()



