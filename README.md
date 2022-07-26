# Price History Web Scrapper
- This program scrapes price information from an online store to produce a historical pricing record. It initially created because Samsung.com doesn't have a price history tool online.I didn't want to refresh the page every day.
- This program's key feature is that it utilizes Selenium to perform any required button presses needed to get a product's price. This is necessary because many sites, like Samsung.com, don't display a product's true price without selecting some options on the product's webpage. 
- This program is parameterize so you can tracker prices for several products given their URL, product name, any button presses you need to perform, and the xpath of the price on the product's URL. All you have to do is add the information to the config.toml file.
- The scraped price data is saved to a local SQLite database which allows for multiple product listings and their price histories to be stored
- Optionally, users can set a target price for their product and if the scraped price is at or below the target, an alert email will be sent to the emails specified in the config.toml file (see instructions below)
- This repository includes a batch file that can be used with Windows Task Scheduler which facilitates automated daily price tracking
- A price alert email is only sent if the user sets up a secure .env file with your gmail credentials

## Requirements
- The lastest Gecko Driver here https://github.com/mozilla/geckodriver/releases
- (OPTIONAL) A Gmail account 

## How to Run
0. Clone this repository into you're local machine and navigate to the folder in your command prompt
1. Install required packages (can also install in an anaconda environment using conda-requirements.txt):
```
pip install -r requirements.txt
```
2. This program utilizes Selenium which requires Gecko Driver to function. If you haven't already done this, please download lastest Gecko Driver here https://github.com/mozilla/geckodriver/releases, unzip it, and add its parent folder to your Windows Path Environment Variable and restart your computer.
3. Modify the values in the "config.toml" file to track the products you are interested in
4. Run "price_tracker_db_setup.py" to set up the SQLite database and tables this program stores price information into
5. Run "price_scrapper_tracker.py" to scrape your first price

## OPTIONAL Set-up: Receive price alert emails if your product is under a specified price
1. In config.toml, add a value to the "target_price" parameter in each "product-info" heading, and a list of "recipients" to the "alert_info" heading.
2. You will need to get an app password from your Gmail account to send emails programmatically: https://support.google.com/accounts/answer/185833?hl=en
3. If you want to email alert, create the file ".env" and add the following information (this information is is a .env file rather than .toml for security reasons)
```
EMAIL_ADDRESS=email@gmail.com
EMAIL_APP_PASSWORD=gmail_app_password
```
4. To confirm email is set-up, set a product's "target_price" in "config.toml" to a large value like 1000000, the run "price_scrapper_tracker.py". A email alert should be sent to the specified recipients if everything was configured correctly. If not, see "app.log" for details about the problem.

## How to schedule the this program to track a listings price history (on Windows machines)
1. Modify the batch file "price_scrapper_tracker_job.bat" to include the correct file/directory paths
2. In the Windows Search Bar, type in "Task Scheduler, open the program, and click "Create Basic Task"
3. Enter your desired name & timing informatino
4. Add the path to the "price_scrapper_tracker_job.bat" to the "Program/Script" option