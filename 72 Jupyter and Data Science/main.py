from bs4 import BeautifulSoup
import requests as req
import csv

res = req.get(
    'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors')
soup = BeautifulSoup(res.text, "html.parser")

headings = [heading.text for heading in soup.select('thead th')]
rows = []

for i in range(32):
    for row in soup.select('tbody tr'):
        new_row = [cell.text for cell in row.select('td .data-table__value')]
        rows.append(new_row)
    res = req.get(
        f'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{i + 1}')
    soup = BeautifulSoup(res.text, "html.parser")

with open('payscale_data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headings)
    writer.writerows(rows)
