import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


logging.basicConfig(filename='scraping_errors.log', level=logging.ERROR)


chrome_options = Options()
chrome_options.page_load_strategy = "eager"  
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-images")

chrome_options.add_argument("--disable-gpu")





chrome_options.add_argument("--remote-debugging-port=9222")

service = Service(executable_path="/mnt/c/Users/madhu/chromedriver-linux64/chromedriver")


output_data = {}


for i in range(1, 12493):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = f"https://indiantradeportal.in/vs.jsp?pid=3&txthscode={i}"
    driver.get(url)


    try:
        australia_checkbox = driver.find_element(By.XPATH, "//label[@class='countryList']//input[@class='getListCountry' and @data-lang='Australia']")
        australia_checkbox.click()


        hs_code_element = driver.find_element(By.XPATH, "//label[@data-hasqtip='397']")
        hs_code = hs_code_element.text.split()[0] 
        time.sleep(3)

        next_button = driver.find_element(By.XPATH, "//input[@type='submit' and @style='float:right;']")
        next_button.click()


        mfn_row = driver.find_element(By.XPATH, "//tr[@class='colorbg agreement7 icolor2']")
        mfn_value = mfn_row.find_elements(By.TAG_NAME, 'td')[1].text  


        output_data[hs_code] = {
            "HS Code": hs_code,
            "MFN": mfn_value
        }
        print(f"HS Code: {hs_code}, MFN: {mfn_value}")

    except Exception as e:
        logging.error(f"Error processing HS Code {i}: {str(e)}")


    if i % 10 == 0:
        with open('hs_mfn_data_2.json', 'w') as json_file:
            json.dump(output_data, json_file, indent=4)
    driver.quit()


with open('hs_mfn_data.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)




print("Data extraction completed and saved to 'hs_mfn_data.json'")