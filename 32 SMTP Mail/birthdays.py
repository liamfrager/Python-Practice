##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.

import datetime as dt
import pandas
import random
import smtplib

now = dt.datetime.now()
birthdays = pandas.read_csv('birthdays.csv').itertuples()
for birthday in birthdays:
    if (now.month, now.day) == (birthday.month, birthday.day):
        name = birthday.name
        email = birthday.email

        with open(f"letter_templates/letter_{random.randint(1, 3)}.txt") as message_file:
            message = message_file.read()
            message = message.replace("[NAME]", name)

            my_email = "liam.frager@gmail.com"
            password = "ywssmwtppzrikwer"

            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs="liam.frager@gmail.com",
                    msg=f"Subject:Happy Birthday!\n\n{
                        message}".encode("UTF-8")
                )
