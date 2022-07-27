from enum import Enum
from pprint import pprint
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from utils.json_parser import parse_json_to_attr


class Page(Enum):
    NONE = 1
    CBO_DIRECTORY = 2
    CARD = 3
    LOGIN = 4
    OTHER = 7


class PageNotFound(Exception):
    pass


class DriverSettings():
    def __init__(self) -> None:
        self.chrome_driver_exe_path = None
        self.webdriver_options = None
        self.driver_timeout = None
        self.user_data_dir = None
        parse_json_to_attr(self, './settings/webdriver_settings.json')

        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={self.user_data_dir}")
        options.page_load_strategy = 'normal'
        [options.add_experimental_option(name, vals) 
            for (name, vals) in self.webdriver_options.items()]

        self.driver = webdriver.Chrome(
            executable_path=self.chrome_driver_exe_path, options=options)
        self.driver.implicitly_wait(self.driver_timeout)

    def get_driver(self):
        return self.driver


class CPXScraper(object):

    CPX_SEARCH_URL = 'https://client.cappex.com/cbo-search'
    CPX_LOGIN_URL = 'https://client.cappex.com/login'
    UNCLICKED_COLOR = '#8e8e8e'

    def __init__(self) -> None:
        # load in webdriver settings and initialize driver
        self.driver = DriverSettings().get_driver()

        # state variables
        self.logged_in = False
        self.page = Page.NONE

    def scrape(self, states: list):
        for state in states:
            all_dict_rows = self.\
                _go_to_search_page()._search_state(state)._scrape_cards()
            save_to_csv(all_dict_rows, state)

            print(f'********************************************')
            print(f'*********** STATE <{state}> DONE ***********')
            print(f'********************************************')

    def go_to_login_page(self):
        self.driver.get(self.CPX_LOGIN_URL)
        self.page = Page.LOGIN
        return self

    def _go_to_search_page(self):
        self.driver.get(self.CPX_SEARCH_URL)
        self.page = Page.CBO_DIRECTORY
        return self

    def _search_state(self, state):
        self._assert_page(Page.CBO_DIRECTORY)
        CBO_location_button = self.driver.find_element(By.ID, 'filter-button--CBO Location')
        CBO_location_button.click()
        state_option = self.driver.find_element(
            By.XPATH, "(//input[contains(@id,'react-select')])[2]")
        state_option.send_keys(state, Keys.ENTER, Keys.ESCAPE)
        return self

    def _scrape_cards(self):
        all_card_row_dicts = []
        has_next_page = True

        while has_next_page:
            cards = self.driver.find_elements(
                By.XPATH, "//div[@data-qa='cbo-card-list']//button"
            )
            for card in cards:
                card_row_info = self._scrape_card(card)
                all_card_row_dicts.append(card_row_info)
                print('\n===========', card_row_info['Name'], 'RESULTS ===========')
                pprint(card_row_info)

            # click next button
            try:
                self.driver.find_element(
                    By.XPATH, "//a[@aria-label='Next page']").click()
            except:
                has_next_page = False

        return all_card_row_dicts

    def _scrape_card(self, card):
        '''Builds one row'''
        print('scraping card...')
        card.click()
        self.page = Page.CARD

        card_window_path = '//div[@role="dialog"]/div'

        row_results = {
            # these get scraped semi-individually
            'Name': None,
            'City': None,
            'State': None,
            'Zip Code': None,
            'Address': None,
            'POC': None,
            'Website': None,
            # these get scraped through 'sections'
            'Program Description': None,
            'Demographics': None,
            'Students Served': None, 
            'Services Offered': None,
            'Matriculation and Completion': None,
            'Colleges Attended by Alumni': None,
            'Scholarships': None # not required
        }

        # MUST BE INCLUDED
        name = self.driver.find_element(
            By.XPATH, card_window_path + '//h5').get_attribute('innerHTML')
        row_results['Name'] = name
        print('card name:', name)
        
        try:
            address = self.driver.find_element(
                By.XPATH, card_window_path + '//h5//following-sibling::p[last()]').get_attribute('innerHTML')
            
            address_cleaned = address.replace(',', '').split(' ')
            city = address_cleaned[-3]
            state_code = address_cleaned[-2]
            zip_code = address_cleaned[-1]
            row_results['Address'] = address
            row_results['City'] = city
            row_results['State'] = state_code
            row_results['Zip Code'] = zip_code
        except Exception as e: 
            print(e)
            address = None
        print('address', address)

        try: poc = ', '.join(
            [elem.get_attribute('innerHTML') for elem in\
                self.driver.find_elements(
                    By.XPATH,
                    "(//div[contains(@class, 'MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-4')])[last()]/div//p[not(a)]"
        )[:-1]] + [self.driver.find_element(
            By.XPATH,
            "(//div[contains(@class, 'MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-4')])[last()]/div//p/a"
            ).get_attribute('innerHTML')
        ])
        except Exception as e: 
            print(e)
            poc = None
        row_results['POC'] = poc
        print('poc', poc)

        try: website = self.driver.find_element(
            By.XPATH, card_window_path + '//a').get_attribute('href')
        except Exception as e:
            print(e)
            website = None
        row_results['Website'] = website
        print('website', website)

        sections = self.driver.find_elements(
            By.XPATH,
            card_window_path + "//div[contains(@class, 'MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-3 MuiGrid-direction-xs-column')]"
        )

        for section in sections:
            try: 
                title = section.find_element(By.TAG_NAME, 'h6').get_attribute('innerHTML')
                print("on section title:", title)
            except: continue

            if title not in row_results:
                print(f'no column for {title}')
                continue

            info = ' '.join([
            elem.get_attribute('innerHTML')\
                for elem in section.find_elements(By.TAG_NAME, 'p')
            ])

            row_results[title] = info

        for (key, value) in row_results.items():
            row_results[key] = clean_string(str(value))

        # exit out of card
        self.driver.find_element(By.XPATH, card_window_path + '//following-sibling::button').click()
        self.page = Page.CBO_DIRECTORY

        return row_results

    def _assert_page(self, *expected_pages):
        """Asserts that current page scraper is on must be one of the 
        expected pages.
        """
        assert self.page in expected_pages, ( 
            f'Expected page to be in { {str(page) for page in expected_pages}}'
            f' but instead was on page {self.page}')


def clean_string(str: str):
    return re.sub('</?[a-z]*>', '', str)

def save_to_csv(dicts: list, filename='info'):
    import pandas as pd

    path = f'./data/{filename}.csv'
    df = pd.DataFrame.from_dict(dicts) 
    df.to_csv (path, index = False, header=True)
