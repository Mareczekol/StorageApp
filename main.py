import os


class Manager:
    def __init__(self):
        self.account = 0
        self.magazyn = {}
        self.actions = []
        self.commands = {
            "saldo": self.saldo,
            "sprzedaz": self.sprzedaz,
            "zakup": self.zakup,
            "konto": self.konto,
            "lista": self.lista,
            "magazyn": self.pokaz_magazyn,
            "przeglad": self.przeglad,
            "koniec": self.koniec
        }
        self.load_data()

    def load_data(self):
        if not os.path.exists('account.txt'):
            with open('account.txt', 'w') as account_file:
                account_file.write('0')
        else:
            with open('account.txt', 'r') as account_file:
                self.account = float(account_file.read().strip())

        if not os.path.exists('inventory.txt'):
            with open('inventory.txt', 'w'):
                pass
        else:
            with open('inventory.txt', 'r') as inventory_file:
                for line in inventory_file:
                    product, price, quantity = line.strip().split(',')
                    self.magazyn[product] = [int(price), int(quantity)]

        if not os.path.exists('actions.txt'):
            with open('actions.txt', 'w'):
                pass
        else:
            with open('actions.txt', 'r') as actions_file:
                for line in actions_file:
                    action = eval(line.strip())
                    self.actions.append(action)

    def execute(self):
        while True:
            print("Dostepne opcje:")
            for command in self.commands.keys():
                print(command)
            command = input("Wybierz opcje: ")
            if command in self.commands:
                self.commands[command]()
            else:
                print("Nieznana komenda")

    def saldo(self):
        amount = float(input("Wprowadz kwote: "))
        if amount < 0 and abs(amount) > self.account:
            print("Nie można odjąć więcej niż jest na koncie")
        else:
            self.account += amount
            self.actions.append(("saldo", amount))
            print("Saldo zaktualizowane")

    def sprzedaz(self):
        product_name = input("Wprowadz nazwe produktu: ")
        price = int(input("Wprowadz cene: "))
        quantity = int(input("Wprowadz ilosc: "))
        if product_name not in self.magazyn:
            print("Brak produktu w magazynie")
        elif price <= 0 or quantity <= 0:
            print("Podaj prawidłową cenę i ilość")
        elif self.magazyn[product_name][1] < quantity:
            print("Nie ma wystarczającej ilości produktu w magazynie")
        else:
            self.account += price * quantity
            self.magazyn[product_name][1] -= quantity
            self.actions.append(("sprzedaz", product_name, price, quantity))
            print("Sprzedaz wykonana")

    def zakup(self):
        product_name = input("Wprowadz nazwe produktu: ")
        price = int(input("Wprowadz cene: "))
        quantity = int(input("Wprowadz ilosc: "))
        if price <= 0 or quantity <= 0:
            print("Nieprawidłowa cena lub ilosc")
        elif self.account < price * quantity:
            print("Nie wystarczające środki na koncie")
        else:
            if product_name not in self.magazyn:
                self.magazyn[product_name] = [price, quantity]
            else:
                self.magazyn[product_name][1] += quantity
            self.account -= price * quantity
            self.actions.append(("zakup", product_name, price, quantity))
            print("Zakup wykonany")

    def konto(self):
        print(f"Stan konta: {self.account}")

    def lista(self):
        print("Stan magazynu:")
        for product, details in self.magazyn.items():
            print(f"Produkt: {product}, Cena: {details[0]}, Ilosc: "
                  f"{details[1]}")

    def pokaz_magazyn(self):
        product_name = input("Wprowadz nazwe produktu: ")
        if product_name in self.magazyn:
            print(f"Produkt: {product_name}, "
                  f"Cena: {self.magazyn[product_name][0]}, "
                  f"Ilosc: {self.magazyn[product_name][1]}")
        else:
            print("Brak produktu w magazynie")

    def przeglad(self):
        start = input("Wprowadz początek zakresu (lub zostaw puste): ")
        end = input("Wprowadz koniec zakresu (lub zostaw puste): ")
        start = int(start) if start else 0
        end = int(end) if end else len(self.actions)
        if start < 0 or end > len(self.actions):
            print("Zakres poza granicami. Dostępne akcje: ", len(self.actions))
        else:
            for action in self.actions[start:end]:
                print(action)

    def koniec(self):
        with open('account.txt', 'w') as account_file:
            account_file.write(str(self.account))

        with open('inventory.txt', 'w') as inventory_file:
            for product, details in self.magazyn.items():
                inventory_file.write(f"{product},{details[0]},{details[1]}\n")

        with open('actions.txt', 'w') as actions_file:
            for action in self.actions:
                actions_file.write(str(action) + '\n')
        exit(0)


if __name__ == "__main__":
    manager = Manager()
    manager.execute()
