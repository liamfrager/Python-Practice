import smtplib
import datetime as dt
import random

now = dt.datetime.now()
if now.weekday() == 1:
    with open('quotes.txt', mode='r') as quotes:
        quote = random.choice(quotes.readlines()).strip()

        my_email = "liam.frager@gmail.com"
        password = "ywssmwtppzrikwer"

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="liam.frager@gmail.com",
                msg=f"Subject:Monday Motivation!\n\n{quote}".encode("UTF-8")
            )
