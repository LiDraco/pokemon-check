import requests
import os
from bs4 import BeautifulSoup
from twilio.rest import Client
from lxml import html
from dotenv import load_dotenv
import time
import logging
import json

count = 0
load_dotenv(verbose=True)
############################################################################################################################################################################################################################################################################################
URL_TO_MONITOR = "https://www.amazon.com/s?k=pokemon+card&i=toys-and-games&rh=n%3A165793011%2Cp_89%3APokemon%2Cp_6%3AATVPDKIKX0DER&s=date-desc-rank&dc&pldnSite=1&qid=1611716828&sa-no-redirect=1&ref=sr_st_date-desc-rank"
DELAY_TIME = 60  # seconds

TWILIO_ACCOUNT_SID = os.getenv("TWILIOSID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIOTOKEN")
TWILIO_PHONE_SENDER = os.getenv("TWILIOSENDER")
TWILIO_PHONE_RECIPIENT = json.loads(os.getenv("TWILIORECIPIENT"))
############################################################################################################################################################################################################################################################################################


def send_text_alert(alert_str):
    """Sends an SMS text alert."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    # single recippient
    # message = client.messages.create(
    #     to=TWILIO_PHONE_RECIPIENT, from_=TWILIO_PHONE_SENDER, body=alert_str
    # )

    # multiple recipients
    for number in TWILIO_PHONE_RECIPIENT:
        message = client.messages.create(
            to=number, from_=TWILIO_PHONE_SENDER, body=alert_str
        )


def webpage_was_changed():
    log = logging.getLogger(__name__)
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s %(message)s"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
        "From": "youremail@domain.com",
    }

    page = requests.get(URL_TO_MONITOR, headers=headers)
    tree = html.fromstring(page.text)
    current = tree.xpath(
        '//*[@id="search"]/span/div/span/h1/div/div[1]/div/div/span[1]/text()'
    )[0].split()[0]
    log.info("Current Count: " + current)
    global count
    if current > count:
        count = current
        return True
    else:
        return False


def main():
    log = logging.getLogger(__name__)
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s %(message)s"
    )
    log.info("Running Website Monitor")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
        "From": "youremail@domain.com",
    }

    page = requests.get(URL_TO_MONITOR, headers=headers)
    tree = html.fromstring(page.text)
    global count
    count = tree.xpath(
        '//*[@id="search"]/span/div/span/h1/div/div[1]/div/div/span[1]/text()'
    )[0].split()[0]
    log.info("Initial Count: " + count)
    while True:
        try:
            if webpage_was_changed():
                log.info("STOCK UPDATE")
                send_text_alert(f"{URL_TO_MONITOR} STOCK UPDATE")
            else:
                log.info("No Stock Change")
        except:
            log.info("Error checking website.")
        time.sleep(DELAY_TIME)


if __name__ == "__main__":
    main()
