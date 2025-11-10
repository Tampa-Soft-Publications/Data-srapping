from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv
from datetime import datetime



# binaries
CHROMIUM_BINARY_PATH = "/usr/bin/chromium"
CHROMIUM_DRIVER_PATH = "/usr/bin/chromedriver" 



chrome_options = Options()


chrome_options.binary_location = CHROMIUM_BINARY_PATH


chrome_options.add_argument("--headless=new") 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


service = Service(executable_path=CHROMIUM_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)


print("Headless Chromium initialized successfully.")



def extract_flight_data(driver):

	flight_data = []



	try:

		table = driver.find_element(By.CLASS_NAME, 'prettyTable.fullWidth')


		rows = table.find_elements(By.TAG_NAME, 'tr')[2:]



		for row in rows:

			cells = row.find_elements(By.TAG_NAME, 'td')

			

			if len(cells) >= 6:

				record = []
				try:

					ident_element = cells[0].find_element(By.TAG_NAME, 'span')

					record.append(ident_element.text.strip())

				except:

					record.append(cells[0].text.strip()) 

				record.append(cells[1].text.strip())


				try:

					origin_span = cells[2].find_element(By.CSS_SELECTOR, 'span[dir="ltr"]')

					record.append(origin_span.text.strip())

				except:

					record.append(cells[2].text.strip()) # Fallback text


				destination_text = ''

				try:

					if cells[3].text.strip():

						destination_span = cells[3].find_element(By.CSS_SELECTOR, 'span[dir="ltr"]')

						destination_text = destination_span.text.strip()

				except NoSuchElementException:

					pass
				record.append(destination_text)




				record.append(cells[4].text.strip())





				record.append(cells[5].text.strip())


				flight_data.append(record)



	except NoSuchElementException:

		print("Error: The flight table was not found. Check the URL and class name.")



	return flight_data


arr = ["FDX", "UPS", "DHK"]
for flight in arr:
	file = open(f'{datetime.now()}_{flight}.csv', 'w')
	csv_writer = csv.writer(file)
	a = []
	number = 0
	headers = ['Ident', 'Type', 'Origin', 'Destination', 'Departure', 'Estimated Arrival Time']
	csv_writer.writerow(headers)
	while True:
		driver.get(f"https://www.flightaware.com/live/fleet/{flight}?;offset={20*number};order=ident;sort=ASC")
		driver.implicitly_wait(5)
		res = extract_flight_data(driver)
		a.append(res)
		csv_writer.writerows(a)
		if (len(res) != 20):
			break
		number = number + 1
		time.sleep(5)
	print("flight")
	file.close()
	time.sleep(150)
driver.quit()
