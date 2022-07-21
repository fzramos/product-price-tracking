# Price History Web Scrapper
- This program scrapes price information from a commerce website to produce a historical pricing record. It initially created because Samsung.com doesn't have a price history tool online and I didn't want to refresh the page every day.
- Selenium is utilized rather than BeautifulSoup because some sites like Samsung.com do not give you a product's price information without clicking a few buttons first
- The scraped data is saved to a local SQLite database which allows for multiple product listings and their prices to be stored
- Future Planned Improvements:
    - Visualize Price History
    - Send an email once a target price is hit
    - Add more error-handling and logging
    - Schedule this program to run on Windows Start-up
    - Create more programs based on "samsung_price_tracker_scrapper.py" for other products/websites

## How to Run
0. Clone this repository into you're local machine and navigate to the folder in your command prompt
1. Install required packages (can also install in an anaconda environment using conda-requirements.txt):
```
pip install -r requirements.txt
```
2. This program utilizes Selenium which requires Gecko Driver to function. If you haven't already done this, please download lastest Gecko Driver here https://github.com/mozilla/geckodriver/releases, unzip it, and add its parent folder to your Windows Path Environment Variable and restart your computer.
3. Run "rice_tracker_db_setup.py" to set up the SQLite database and tables this program stores price information into
4. Run "samsung_price_tracker_scrapper.py" to scrape your first price
5. (Recommended) Schedule "samsung_price_tracker_scrapper.py" to run daily
