from bs4 import BeautifulSoup

from shop.api_clients import BaseClient


class Parser(BaseClient):
    base_url = 'https://easysneakersstore.com/collections/air-jordan'

    def parse(self):
        response = self._request(
            method='get'
        )
        soup = BeautifulSoup(response)
        breakpoint()
        for element in soup.find_all('div', attrs={'class': 'usf-sr-product Grid__Cell 1/2--phone 1/3--tablet-and-up 1/4--desk'}):
            ...
            breakpoint()

parser = Parser()
