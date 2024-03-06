MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

profit = 0


def toggle_power():
  """Toggles whether the machine is on or off."""
  global is_on
  is_on = False if is_on else True
  print(f"Powering {'on' if is_on else 'off'}...")


def report():
  """Reports the current resources of the coffee machine."""
  print(f"Water: {resources['water']}ml")
  print(f"Milk: {resources['milk']}ml")
  print(f"Coffee: {resources['coffee']}mg")
  print(f"Money: ${profit}")



def can_make_order(order):
  """Takes an order and returns a Bollean indicating whether there are sufficient resources to make the drink."""
  ingredients = MENU[order]['ingredients']
  for ingredient in ingredients:
    if resources[ingredient] < ingredients[ingredient]:
      print(f"Sorry there is not enough {ingredient}.")
      return False
  return True


def accept_payment(order):
  """Takes an order, prompts payment from the user, and returns a Boolean indicating whether the payment was sufficient."""
  price = MENU[order]['cost']
  quarters = int(input("How many quarters?: "))
  dimes = int(input("How many dimes?: "))
  nickels = int(input("How many nickels?: "))
  pennies = int(input("How many pennies?: "))
  payment = quarters * .25 + dimes * .1 + nickels * .05 + pennies * .01
  if payment < price:
    print("​Sorry that's not enough money. Money refunded.​")
    return False
  elif payment > price:
    change = "{:.2f}".format(payment - price)
    print(f"Here is ${change} in change.")
    return True
  else:
    return True


def make_drink(order):
  """Takes an order, adds it's price to profit, and removes the required ingredients from resources."""
  global profit
  profit += MENU[order]['cost']
  ingredients = MENU[order]['ingredients']
  for ingredient in ingredients:
    resources[ingredient] -= MENU[order]['ingredients'][ingredient]
  print(f"Here is your {order}. ☕️ Enjoy!")
  
is_on = False
toggle_power()
while is_on:
  order = input("​What would you like? (espresso/latte/cappuccino): ").lower()
  if order == 'off':
    toggle_power()
  elif order == 'report':
    report()
  else:
    if order in MENU:
      if can_make_order(order):
        if accept_payment(order):
          make_drink(order)
    else:
      print("Not a valid order. Please try again.")
  