from src.scraper import CPXScraper, clean_string, save_to_csv

if __name__ == "__main__":
    bot = CPXScraper().go_to_login_page()

    if(input(
        'Enter "c" to continue after you have logged in manually: ') == 'c'):
        bot.scrape([
            # TODO(pforderique): Kansas gets mistaken for AK. 
            #   Update scraper to select correct option. 
            #   Manually select this one for now.
            # 'Kansas', 

            # 'District of Columbia', 
            # 'Delaware', 
            # 'Texas',
            # 'Missouri',
            # 'Arizona', 
            # 'New Mexico', 
            # 'Tennessee', 
            # 'Alabama', 
            # 'Florida', 
            # 'North Carolina', 
            # 'South Carolina',
            # 'Louisiana',
            # 'California',
            # 'Colorado',
            # 'Missouri', 
            # 'Illinois',
            # 'Oregon',
            # 'Minnesota',
            # 'Wisconsin',
            # 'New York',
            # 'Washington',
            'Wisconsin',
        ])