a = []
import time

import json

for i in range(589):
    a.append("https://dummydatabase.org"+str(i*10))

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36"
}
d = open("airlines.json", 'w')
for i in a:
    html = requests.get(i, headers=headers)
    while True:
        if html.status_code == 200:
            break
        else:
            html = requests.get(i, headers=headers)
            print(html)
            time.sleep(5)
            
    soup = BeautifulSoup(html.text, 'html.parser')
    print(html)
    target_class = "table"

    table = soup.find("table", class_=target_class)

    if table:
        tbody = table.find("tbody")
        if tbody:

            for row in tbody.find_all("tr"):
                cell = [td.get_text(strip=True) for td in row.find_all('td')]
                c = []
                for k in cell:
                    c.append(k)
                airline_data = {
    "Name": c[0],
    "IATA": c[1],
    "ICAO": c[2],
    "CallSign": c[3],
    "Country": c[4],
    "Active": c[5]
}
                d.write(str(airline_data)+"\n")
                
        else:
            print("No <tbody> found in the table.")
            print(i)
            break
    else:
        print(f"No table found with class '{target_class}'.")
        print(i)
        break


d.close()
            
