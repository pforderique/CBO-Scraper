from src.scraper import CPXScraper, clean_string, save_to_csv

if __name__ == "__main__":
    # print(clean_string('<span>hi</span>'))
    # save_to_csv([{'name': 'fab', 'age': 22}, {'name': 'Dre', 'age': 25}])
    bot = CPXScraper()\
        .go_to_login_page()

    if(input('Enter "c" to continue after logging in:') == 'c'):
        bot.scrape([
            # 'District of Columbia', 
            # 'Delaware', 
            # 'Texas',
            # 'Missouri',
            # 'Kansas', # mistakes with AK
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
            'Missouri', 
            'Illinois',
            'Oregon',
        ])