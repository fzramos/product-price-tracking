# Price History Web Scrapper
- This program scrapes price information from a commerce website to produce a historical pricing record. It initially created because Samsung.com doesn't have a price history tool online and I didn't want to refresh the page every day.
- Selenium is utilized rather than BeautifulSoup because some sites like Samsung.com do not give you a product's price information without clicking a few buttons first
- The scraped price data is saved to a local SQLite database which allows for multiple product listings and their prices to be stored
- Users can set a target price for their product and if the scraped price is at or below the target an alert email will be sent to specified email addresses
- This repository includes a batch file that can be used with Windows Task Scheduler which facilitates automated daily price tracking

## Requirements
- Windows 10+ Machine
- Microsoft Outlook
- The lastest Gecko Driver here https://github.com/mozilla/geckodriver/releases

## How to Run
0. Clone this repository into you're local machine and navigate to the folder in your command prompt
1. Install required packages (can also install in an anaconda environment using conda-requirements.txt):
```
pip install -r requirements.txt
```
2. This program utilizes Selenium which requires Gecko Driver to function. If you haven't already done this, please download lastest Gecko Driver here https://github.com/mozilla/geckodriver/releases, unzip it, and add its parent folder to your Windows Path Environment Variable and restart your computer.
3. Modify the values in the "config.ini" file to track the product you are interested in
3. Run "price_tracker_db_setup.py" to set up the SQLite database and tables this program stores price information into
4. Run "samsung_price_tracker_scrapper.py" to scrape your first price

## How to schedule the this program to track a listings price history
1. Modify the batch file "samsung_price_tracker_job.bat" to include the correct file/directory paths
2. In the Windows Search Bar, type in "Task Scheduler, open the program, and click "Create Basic Task"
3. Enter your desired name & timing informatino
4. Add the path to the "samsung_price_tracker_job.bat" to the "Program/Script" option