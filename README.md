# Price History Web Scrapper
- This program scrapes price information from a commerce website to produce a historical pricing record. It initially created because Samsung.com doesn't have a price history tool online.I didn't want to refresh the page every day.
- This program's key feature is that it utilizes Selenium to perform any website button presses needed to get a product's price. This is necessary because many sites, like Samsung.com, don't display a product's true price without selecting some options on the product website. 
- This program is parameterize so you can tracker prices for several products given their URL, product name, any button presses you need to perform, and the xpath of the price on the product's URL. All you have to do is add the information to the config.toml file.
- The scraped price data is saved to a local SQLite database which allows for multiple product listings and their price histories to be stored
- Users can set a target price for their product and if the scraped price is at or below the target, an alert email will be sent to the emails specified in the config.toml file
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
4. Run "price_scrapper_tracker.py" to scrape your first price

## How to schedule the this program to track a listings price history
1. Modify the batch file "price_scrapper_tracker_job.bat" to include the correct file/directory paths
2. In the Windows Search Bar, type in "Task Scheduler, open the program, and click "Create Basic Task"
3. Enter your desired name & timing informatino
4. Add the path to the "price_scrapper_tracker_job.bat" to the "Program/Script" option