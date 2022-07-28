# CBO Bot

## How to run
1. Update the `chrome_driver_exe_path` and `user_data_dir` fields in `settings/web_driver_settings.json` to point to your [chromedriver](https://chromedriver.chromium.org/downloads) and some temp folder, respectively.
2. Edit `main.py` to scrape for the desired states.
3. Run `main.py`. You will be promted to enter "c" on program start. Because [Cappex](https://client.cappex.com/cbo-search) uses captcha, you will need to login to the site using your own credentials. Once logged in, enter "c" into the terminal and the scraper will continue. Each state will output results in the `data/` folder (you may need to manually create it in your root directory) and be named `<state-name-here>.csv`.

## Contact
For technical support, please contact Piero Fabrizzio Orderique at <porderiq@mit.edu>.