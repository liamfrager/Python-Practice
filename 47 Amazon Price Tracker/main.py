from bs4 import BeautifulSoup
import requests as req
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
MY_EMAIL = "liam.frager@gmail.com"

res = req.get(
    url="https://www.amazon.com/Kasa-Smart-KS200P3-Required-Certified/dp/B0BTMVQK7C/ref=sr_1_2?crid=16GLT8N5RL4IQ&dib=eyJ2IjoiMSJ9.ce_4uQYALXN-37TQwTueV4qU4s5Lznu5PPZE6OJOgBbPgG53-Po91lYS6Y4kuj3geccmmCmYuFzXzUKd_KZLAtwmCx7a00AslWyBjsMGfgIX47_7esvN7W0nxkkjkm3_yVtGqZFnxgDlpAfmJ3eS-rp3gwqtZqxKi6MIRd3oySYjL4dOlXO6IDkzDDYb8rEo4OHAL7NiijYZqXYHw0f9a5TZDcfZN0o-BroMqHwx-C3ctdMJxbz9f6kfrYG341mYO63j9dNcsaB2nDqMw2QItG88dNp-fMiXxLy9mvyB9Fo.PTg9RrEpiRsXzw_b6rPR3qzH-0uE2sSDb_Tzm6oKKNM&dib_tag=se&keywords=smart%2Blight%2Bswitches&qid=1710176152&sprefix=smartlight%2Caps%2C219&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
    headers={
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
)
amazon_page = res.text

soup = BeautifulSoup(amazon_page, "html.parser")


product_name = soup.select_one("#productTitle").getText().strip()
product_price = float(soup.select_one(".a-price-whole").getText() +
                      soup.select_one(".a-price-fraction").getText())

if product_price < 50:
    with smtplib.SMTP('smtp.gmail.com:587') as s:
        s.starttls()
        s.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
        s.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: Price Alert!\n\nThe price for {product_name} has dropped to {product_price} on Amazon!"
        )
    print("Message sent!")
