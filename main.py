from src.scraper import CPXScraper, clean_string, save_to_csv

if __name__ == "__main__":
    bot = CPXScraper().go_to_login_page()

    if(input('Enter "c" to continue after logging in:') == 'c'):
        bot.scrape([
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
            # 'Kansas', # mistakes with AK. Manually select this one.
            'Minnesota',
            'Wisconsin',
            'Washington',
            'New York',
        ])