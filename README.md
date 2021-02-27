# Pokemon Check

pokemon-check is a stock checking program that checks amazon for restocks on Pokemon cards being sold at MSRP by monitoring for changes in specific elements on the page that indicate stock count.

This program can be easily modified to monitor any element on a website and notify if any changes occur

## Installation

Use pip to install the required packages.

We will use
- **lxml** to get the elements via xpath ```pip install lxml ```
- **dotenv** for our enviroment variables ```pip install python-dotenv```
- **twilio** for SMS notifications (optional) ```pip install twilio```

## SMS Notifications

[Twilio](https://www.twilio.com/) is used to notify the user with SMS notifications should any changes occur.
To set up Twilio notifications create an account and create a dotenv file to store your 
- Twilio SID
- Twilio Auth Token
- Sender # (Provided by Twilio)
- Receiver #

## Changing the site/element

In order to change the site being monitored just replace the link in URL_TO_MONITOR.

To change the elements being monitored, replace the two lines with the xpath to your desired element
```python
count = tree.xpath('//*[@id="search"]/span/div/span/h1/div/div[1]/div/div/span[1]/text()')
```

## License

[MIT](https://choosealicense.com/licenses/mit/)