from bs4 import BeautifulSoup
import requests


class GetAmazonProductPrice:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        self.possible_price_ele_id = [
            'priceblock_pospromoprice', 'price_inside_buybox']
        self.possible_price_ele_class = ['a-color-price']
        self.the_price = ""

    def initial_config(self):
        r = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        return BeautifulSoup(soup.prettify(), "html.parser")

    def search_by_id(self):
        if not self.the_price:
            for id in self.possible_price_ele_id:
                check_id = self.initial_config().find(id=id)
                if check_id:
                    self.the_price = check_id.get_text()
                    break

    def search_by_class(self):
        if not self.the_price:
            for className in self.possible_price_ele_class:
                check_class = self.initial_config().find(class_=className)
                if check_class:
                    self.the_price = check_class.get_text()
                    break

    def get_price(self):
        self.search_by_id()
        self.search_by_class()

        if self.the_price:
            return str(self.the_price)
        return None

    def __str__(self):

        price_split = self.get_price().strip().split()

        currency = ""
        price = 0.0

        if price_split[0]:
            currency = price_split[0]
        if price_split[1]:
            price = float(price_split[1])

        return str({
            "currency": currency,
            "price": price
        })


print(GetAmazonProductPrice(
    'https://www.amazon.com/-/es/Apple-iPhone-32-GB-Renovado/dp/B01N4R20RS/ref=lp_18637575011_1_1?srs=18637575011&ie=UTF8&qid=1583701287&sr=8-1'))
