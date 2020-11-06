from enum import Enum


class BuyOrSell(Enum):
    BUY = 'BUY'
    SELL = 'SELL'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

if __name__ == '__main__':
    print(BuyOrSell.BUY.value)
    print(BuyOrSell.choices())
