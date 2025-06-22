from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import time
import re


def parse(line):
    # description =
    price_match = re.search(r"From ([\d,]+) US dollars", line)
    if price_match:
        price = price_match.group(1)
        print(f"Price: {price}")

    airline_match = re.search(r"flight with\s+(.*?)(?=\.)", line)
    if airline_match:
        airline = airline_match.group(1)
        print(f"Airline: {airline}")

    time_date_match = re.findall(
        r"(\d{1,2}:\d{2}\s?[APMapm]{2}\s+on\s+\w+,\s+\w+\s+\d{1,2})", line
    )
    if time_date_match:
        depart_time_date = time_date_match[0]
        print(f"Departure: {depart_time_date}")
        arrive_time_date = time_date_match[1]
        print(f"Arrival: {arrive_time_date}")
    return ""


def flight_monitor(location, depart_date, return_date):
    if depart_date > return_date:
        return

    driver = webdriver.Chrome()
    driver.get("http://www.google.com/travel/flights")

    passengers = driver.find_element(
        By.XPATH,
        "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/div/button",
    )
    passengers.click()
    time.sleep(0.5)

    add_adult = driver.find_element(By.XPATH, '//*[@aria-label="Add adult"]')
    add_adult.click()
    add_adult.send_keys(Keys.ESCAPE)
    time.sleep(0.5)

    where_to = driver.find_element(By.XPATH, '//input[@aria-label="Where to? "]')
    where_to.send_keys(location)
    time.sleep(0.5)

    list_item = driver.find_element(
        By.XPATH,
        "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[3]/ul/li[1]",
    )
    list_item.click()

    time.sleep(0.5)

    departure = driver.find_element(By.XPATH, '//*[@aria-label="Departure"]')
    departure.send_keys(depart_date)
    time.sleep(0.5)

    ret_date = driver.find_element(By.XPATH, '//*[@aria-label="Return"]')
    ret_date.send_keys(return_date)
    ret_date.send_keys(Keys.ENTER)
    time.sleep(0.5)

    search = driver.find_element(By.XPATH, '//*[@aria-label="Search"]')
    search.click()
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    for li in soup.find_all("li"):
        divs = li.find_all("div")
        if len(divs) > 1:
            aria = divs[1].get("aria-label")
            if aria and aria.startswith("From"):
                # print(aria)
                parse(aria)
                break

    driver.close()


if __name__ == "__main__":
    flight_monitor("Ho Chi Minh City, Vietnam", "03/13", "03/27")
