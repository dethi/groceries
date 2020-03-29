from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup


@dataclass
class BasketItem:
    quantity: int
    product: str
    unit_price: int


def parse_email(content: str) -> List[BasketItem]:
    soup = BeautifulSoup(content, "html.parser")

    headers = soup.find_all("th")
    table_el = headers[-1].find_parent("table")
    tbody_el = table_el.find("tbody")
    rows = tbody_el.find_all("tr")

    basket = []
    for row in rows:
        cols = [c.text.strip() for c in row.find_all("td")]
        quantity = int(cols[0])
        product = cols[1]
        unit_price = int(float(cols[2].lstrip("€")) * 100)

        basket.append(BasketItem(quantity, product, unit_price))

    return basket
