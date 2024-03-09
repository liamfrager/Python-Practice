import datetime as dt
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:
    def __init__(self):
        self.from_email = "liam.frager@gmail.com"
        self.from_password = os.environ["GMAIL_PASSWORD"]
    # This class is responsible for sending notifications with the deal flight details.

    def notify_flight(self, flight):
        depart = flight["flyFrom"]
        arrive = flight["flyTo"]
        price = flight["price"]
        date = flight["local_departure"].split("T")[0].split("-")
        date = [int(n) for n in date]
        date = dt.date(date[0], date[1], date[2]).strftime("%B %-d")
        return f"There is a flight from {depart} 🛫 to 🛬 {arrive} for ${price} on {date}\n"

    def send_email(self, message):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.from_email, password=self.from_password)
            connection.sendmail(
                from_addr=self.from_email,
                to_addrs=self.from_email,
                msg=f"Subject:Flight Deals\n\n{message}".encode("UTF-8")
            )
