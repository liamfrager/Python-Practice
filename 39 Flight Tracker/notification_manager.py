import datetime as dt


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def notify_flight(self, flight):
        depart = flight["flyFrom"]
        arrive = flight["flyTo"]
        price = flight["price"]
        date = flight["local_departure"].split("T")[0].split("-")
        date = [int(n) for n in date]
        date = dt.date(date[0], date[1], date[2]).strftime("%B %-d")
        print(f"There is a flight from {depart} 🛫 to 🛬 {arrive} for ${price} on {date}")
