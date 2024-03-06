from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
print("\n")

MENU = Menu()
COFFEE_MAKER = CoffeeMaker()
MONEY_MACHINE = MoneyMachine()

is_on = True
while is_on:
  order = input(f"What would you like? ({MENU.get_items()[:-1]}): ").lower()
  if order == 'off':
    is_on = False
  elif order == 'report':
    COFFEE_MAKER.report()
    MONEY_MACHINE.report()
  else:
    drink = MENU.find_drink(order)
    print(f"{'An' if drink.name == 'espresso' else 'A'} {drink.name} costs ${"{:.2f}".format(drink.cost)}.")
    if COFFEE_MAKER.is_resource_sufficient(drink) and MONEY_MACHINE.make_payment(drink.cost):
      COFFEE_MAKER.make_coffee(drink)
  print()