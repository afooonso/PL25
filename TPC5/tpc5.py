from dataclasses import dataclass
from datetime import datetime
import json
import ply.lex as lex
from tabulate import tabulate

@dataclass
class Product:
    code: str
    name: str
    quantity: int
    price: float

def format_balance(balance):
    integer_part = int(balance)
    decimal_part = int(round((balance - integer_part) * 100))
    if decimal_part == 0:
        return f"{integer_part}e"
    if integer_part == 0:
        return f"{decimal_part:02d}c"
    return f"{integer_part}e{decimal_part:02d}c"

coins = [2.00, 1.00, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01]

def get_balance_in_coins(balance) -> list[int]:
    result = []
    for coin in coins:
        result.append(int(balance // coin))
        balance %= coin
    return result

class VendingMachine:
    tokens = (
        'SHOW_PRODUCTS',
        'BALANCE',
        'EXIT',
        'COIN_VALUE',
        'PRODUCT_CODE',
    )

    states = (
        ('insertcoin', 'exclusive'),
        ('selectproduct', 'exclusive'),
    )

    t_ANY_ignore = ' \t\n'
    t_insertcoin_ignore = ', \t\n'

    def __init__(self):
        self.lexer = None
        self.exit_flag = False
        self.balance = 0.0
        self.inventory = []
        self.load_inventory()
        date = datetime.now().strftime("%Y-%m-%d")
        self.display_message(f"{date}, Inventory loaded, System ready.")
        self.display_message("Hello there! Ready to take your order.")

    def load_inventory(self):
        with open("stock.json", encoding="utf8") as f:
            self.inventory = [Product(**p) for p in json.load(f)]

    def save_inventory(self):
        with open("stock.json", "w", encoding="utf8") as f:
            json.dump([p.__dict__ for p in self.inventory], f, ensure_ascii=False, indent=4)

    def t_begin_insertcoin(self, t):
        r'INSERT'
        t.lexer.begin('insertcoin')

    def t_insertcoin_COIN_VALUE(self, t):
        r'2e|1e|50c|20c|10c|5c|2c|1c'
        if t.value[-1] == 'c':
            t.value = int(t.value[:-1]) / 100
        elif t.value[-1] == 'e':
            t.value = int(t.value[:-1])
        self.balance += t.value
        return t

    def t_insertcoin_exit(self, t):
        r'\.'
        self.show_balance()
        t.lexer.begin('INITIAL')

    def t_begin_selectproduct(self, t):
        r'SELECT'
        t.lexer.begin('selectproduct')

    def t_selectproduct_PRODUCT_CODE(self, t):
        r'[A-Z][0-9]{2}'
        t.lexer.begin('INITIAL')
        for product in self.inventory:
            if product.code == t.value:
                if product.quantity <= 0:
                    self.display_message(f"Product {product.name} is out of stock.")
                    return t
                if product.price > self.balance:
                    self.display_message(f"Insufficient balance for \"{product.name}\" (requires {format_balance(product.price)})")
                    self.show_balance()
                    return t
                self.balance -= product.price
                product.quantity -= 1
                self.display_message(f"Please collect your \"{product.name}\".")
                self.show_balance()
                return t
        self.display_message("Invalid product code.")
        return t

    def t_ANY_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def t_SHOW_PRODUCTS(self, t):
        r'SHOW'
        self.display_message("")
        print(tabulate([[p.code, p.name, p.quantity, p.price] for p in self.inventory],
                       headers=["Code", "Name", "Quantity", "Price"]))
        return t

    def t_BALANCE(self, t):
        r'BALANCE'
        self.show_balance()
        return t

    def show_balance(self):
        self.display_message(f"Balance:", format_balance(self.balance))

    def t_EXIT(self, t):
        r'EXIT'
        self.exit_flag = True
        change = [f"{n}x {format_balance(coins[i])}" for i, n in enumerate(get_balance_in_coins(self.balance)) if n > 0]
        if change:
            self.display_message("Please collect your change: " + ", ".join(change))
        self.display_message("Goodbye!")
        self.save_inventory()
        return t

    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    def process_input(self, data):
        self.lexer.input(data)

    def get_token(self):
        return self.lexer.token()

    def display_message(self, *content):
        print("Vending Machine:", *content)

def main():
    machine = VendingMachine()
    machine.build()

    while not machine.exit_flag:
        user_input = input(">> ")
        machine.process_input(user_input)
        while True:
            token = machine.get_token()
            if not token:
                break

if __name__ == '__main__':
    main()