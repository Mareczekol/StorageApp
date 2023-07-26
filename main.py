import os


class Manager:
    def __init__(self, execute, assign):
        self.account = 0
        self.magazyn = {}
        self.actions = []
        self.commands = {}
        self.execute = execute
        self.assign = assign
        self.exit_flag = False

    def assign_command(self, name):
        def decorator(cb):
            self.commands[name] = cb
        return decorator

    def execute_command(self, name):
        while True:
            print("Dostepne opcje:")
            for command in self.commands.keys():
                print(command)
            command = input("Wybierz opcje: ")
            if command == "koniec":
                if self.exit_flag:
                    break
                else:
                    self.exit_flag = True
            if command in self.commands:
                self.commands[command]()
            else:
                print("Nieznana komenda")
            print()


def load_data(manager):
    if not os.path.exists('account.txt'):
        with open('account.txt', 'w') as account_file:
            account_file.write('0')
    else:
        with open('account.txt', 'r') as account_file:
            manager.account = float(account_file.read().strip())

    if not os.path.exists('inventory.txt'):
        with open('inventory.txt', 'w'):
            pass
    else:
        with open('inventory.txt', 'r') as inventory_file:
            for line in inventory_file:
                product, price, quantity = line.strip().split(',')
                manager.magazyn[product] = [int(price), int(quantity)]

    if not os.path.exists('actions.txt'):
        with open('actions.txt', 'w'):
            pass
    else:
        with open('actions.txt', 'r') as actions_file:
            for line in actions_file:
                action = eval(line.strip())
                manager.actions.append(action)


def save_data(manager):
    with open('account.txt', 'w') as account_file:
        account_file.write(str(manager.account))

    with open('inventory.txt', 'w') as inventory_file:
        for product, details in manager.magazyn.items():
            inventory_file.write(f"{product},{details[0]},{details[1]}\n")

    with open('actions.txt', 'w') as actions_file:
        for action in manager.actions:
            actions_file.write(str(action) + '\n')


manager = Manager(load_data, Manager.assign_command)


@manager.assign_command("saldo")
def saldo():
    amount = float(input("Wprowadz kwote: "))
    if amount < 0 and abs(amount) > manager.account:
        print("Nie można odjąć więcej niż jest na koncie")
    else:
        manager.account += amount
        manager.actions.append(("saldo", amount))
        print("Saldo zaktualizowane")


@manager.assign_command("sprzedaz")
def sprzedaz():
    product_name = input("Wprowadz nazwe produktu: ")
    price = int(input("Wprowadz cene: "))
    quantity = int(input("Wprowadz ilosc: "))
    if product_name not in manager.magazyn:
        print("Brak produktu w magazynie")
    elif price <= 0 or quantity <= 0:
        print("Podaj prawidłową cenę i ilość")
    elif manager.magazyn[product_name][1] < quantity:
        print("Nie ma wystarczającej ilości produktu w magazynie")
    else:
        manager.account += price * quantity
        manager.magazyn[product_name][1] -= quantity
        manager.actions.append(("sprzedaz", product_name, price, quantity))
        print("Sprzedaz wykonana")
        if manager.magazyn[product_name][1] == 0:
            del manager.magazyn[product_name]


@manager.assign_command("zakup")
def zakup():
    product_name = input("Wprowadz nazwe produktu: ")
    price = int(input("Wprowadz cene: "))
    while True:
        quantity_input = input("Wprowadz ilosc (lub zostaw puste aby anulować): ")
        if not quantity_input:
            break
        try:
            quantity = int(quantity_input)
            if quantity <= 0:
                print("Nieprawidłowa ilość")
            else:
                if product_name not in manager.magazyn:
                    manager.magazyn[product_name] = [price, quantity]
                else:
                    manager.magazyn[product_name][1] += quantity
                    manager.account -= price * quantity
                    manager.actions.append(("zakup", product_name, price, quantity))
                    print("Zakup wykonany")
                if manager.magazyn[product_name][1] == 0:
                    del manager.magazyn[product_name]
                break
        except ValueError:
            print("Nieprawidłowa ilość")


@manager.assign_command("konto")
def konto():
    print(f"Stan konta: {manager.account}")


@manager.assign_command("lista")
def lista():
    print("Stan magazynu:")
    for product, details in manager.magazyn.items():
        print(f"Produkt: {product}, Cena: {details[0]}, Ilosc:{details[1]}")


@manager.assign_command("magazyn")
def pokaz_magazyn():
    product_name = input("Wprowadz nazwe produktu: ")
    if product_name in manager.magazyn:
        print(f"Produkt: {product_name}, "
              f"Cena: {manager.magazyn[product_name][0]}, "
              f"Ilosc: {manager.magazyn[product_name][1]}")
    else:
        print("Brak produktu w magazynie")


@manager.assign_command("przeglad")
def przeglad():
    start = input("Wprowadz początek zakresu (lub zostaw puste): ")
    end = input("Wprowadz koniec zakresu (lub zostaw puste): ")
    start = int(start) if start else 0
    end = int(end) if end else len(manager.actions)
    if start < 0 or end > len(manager.actions):
        print("Zakres poza granicami. Dostępne akcje: ", len(manager.actions))
    else:
        for action in manager.actions[start:end]:
            print(action)


@manager.assign_command("koniec")
def koniec():
    save_data(manager)
    manager.exit_flag = True


if __name__ == "__main__":
    load_data(manager)
    while True:
        print("Dostępne komendy:")
        for command in manager.commands.keys():
            print(command)
        print()
        command = input("Wybierz opcję: ")
        manager.execute_command(command)
        if manager.exit_flag:
            break
