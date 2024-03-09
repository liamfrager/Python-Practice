# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import datetime as dt
from flight_search import FlightSearch
from notification_manager import NotificationManager
from data_manager import DataManager
from signup import Users

message = ""

today = dt.date.today()
search_frame = today + dt.timedelta(6*30)

data_manager = DataManager()
data_manager.update_iata_codes()
search_locations = data_manager.get_locations()
for location in search_locations:
    destination = location["iataCode"]
    message += destination.upper() + "\n"
    max_price = int(location["lowestPrice"])
    flight_params = {
        "fly_from": "BOS",
        "fly_to": destination,
        "date_from": today.strftime("%d/%m/%Y"),
        "date_to": search_frame.strftime("%d/%m/%Y"),
        "adults": 2,
        "price_to": max_price,
        "curr": "USD",
    }
    flight_search = FlightSearch()
    flights = flight_search.search_flights(flight_params)
    if len(flights) == 0:
        message += f"There are no cheap flights to {destination} available right now."
    else:
        notify = NotificationManager()
    for flight in flights:
        message += notify.notify_flight(flight)
users = Users().get_users()
for user in users:
    notify.send_email(message)
