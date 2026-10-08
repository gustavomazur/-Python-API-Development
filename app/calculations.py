def add(numero1: int, numero2: int):
    return numero1 + numero2


def subtract(numero1: int, numero2: int):
    return numero1 - numero2

def multiply(numero1: int, numero2: int):
    return numero1 * numero2

def divide(numero1: int, numero2: int):
    return numero1 / numero2



class InssufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InssufficientFunds("insufficient funds in account")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1

    