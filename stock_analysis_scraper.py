# Scraper for Stockanalysis.com

import os
import json

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time

# Pandas
import pandas as pd
import numpy as np

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-popup-blocking")
# chrome_options.add_argument("--headless") NOTE: Running in headless will result in empty dataframes.
chrome_options.add_argument("--disable-gpu")


xpaths = {
    "col": [
        "/html/body/div/div[1]/div[2]/main/div[5]/table/thead/tr/th[{}]",
        "/html/body/div/div[1]/div[2]/main/div[4]/table/thead/tr/th[{}]",
    ],
    "row": [
        "/html/body/div/div[1]/div[2]/main/div[5]/table/tbody/tr[{}]/td[1]",
        "/html/body/div/div[1]/div[2]/main/div[4]/table/tbody/tr[{}]/td[1]",
    ],
    "header": [
        "/html/body/div/div[1]/div[2]/main/div[5]/table/thead/tr/th[{}]",
        "/html/body/div/div[1]/div[2]/main/div[4]/table/thead/tr/th[1]",
    ],
    "qtr_button": "/html/body/div/div[1]/div[2]/main/div[2]/nav[2]/ul/li[2]/button",
}


class StockAnalysis:
    def __init__(
        self, ticker: str, halt_scrape: bool = False, log_data: bool = False
    ) -> None:
        self.halt_scrape = (
            halt_scrape  # Determine if scraping is stopped if element is not found.
        )
        self.ticker = ticker.upper()
        self.chrome_driver = self._get_chrome_driver_path()
        self.base_export_path = self._get_data_export_path()
        # Make directory for statements.
        os.makedirs(self.base_export_path, exist_ok=True)
        self.ticker_folder = f"{self.base_export_path}\\{self.ticker}"
        # Make a folder for the ticker.
        os.makedirs(self.ticker_folder, exist_ok=True)
        # Make a folder for "Annual" and "Quarter" statements.
        os.makedirs(f"{self.ticker_folder}\\Annual", exist_ok=True)
        os.makedirs(f"{self.ticker_folder}\\Quarter", exist_ok=True)
        self.log_data = log_data
        # Variables for financial statements.
        self.income_statement = pd.DataFrame()
        self.balance_sheet = pd.DataFrame()
        self.cash_flow = pd.DataFrame()
        self.earnings = pd.DataFrame()

        self.quarter_params = ["Quarter", "quarter", "Quarterly", "quarterly", "Q", "q"]
        self.annual_params = ["Annual", "annual", "A", "a"]

    """-----------------------------------"""

    def _get_data_export_path(self):
        with open("config.json", "r") as file:
            data = json.load(file)
        return data["data_export_path"]

    """-----------------------------------"""

    def _get_chrome_driver_path(self):
        with open("config.json", "r") as file:
            data = json.load(file)
        return data["chrome_driver_path"]

    ################################################################### Browser Creation
    def create_browser(self, url=None):
        """
        :param url: The website to visit.
        :return: None
        """
        service = Service(executable_path=self.chrome_driver)
        self.browser = webdriver.Chrome(service=service, options=chrome_options)
        # Default browser route
        if url == None:
            self.browser.get(url=self.sec_quarterly_url)
        # External browser route
        else:
            self.browser.get(url=url)

    ################################################################### Statement Scraping
    def scrape_income_statement(self, freq: str = "q"):
        """
        Scrape the income statement table from Stockanalysis.com

        Parameters
        ----------
        ticker : str
           Ticker of the company
        freq : str, optional
            Frequency of data. In Annual(a) or Quarter(q) format, by default "q"

        Returns
        -------
        DataFrame
            Dataframe representing the table scraped.
        """
        if freq in self.annual_params:
            freq = "a"
            url = f"https://stockanalysis.com/stocks/{self.ticker.lower()}/financials/"
            self.create_browser(url)

        elif freq in self.quarter_params:
            freq = "q"
            url = f"https://stockanalysis.com/stocks/{self.ticker.lower()}/financials/?p=quarterly"
            self.create_browser(url)
            qtr_button_xpath = xpaths["qtr_button"]
            self.click_button(qtr_button_xpath, wait=True, wait_time=10)
        df = self.get_table(freq=freq, display_dimenstions=True)
        self._clean_close()
        return df

    def get_income_statement(self, freq: str = "q"):
        folder = self._get_period_folder(freq)
        path = f"{self.ticker_folder}\\{folder}\\income_statement.csv"
        try:
            df = pd.read_csv(path)
            df.rename(columns={"Unnamed: 0": "index"}, inplace=True)
            df.set_index("index", inplace=True)
            return df
        except FileNotFoundError:
            df = self.scrape_income_statement(freq)
            df.to_csv(path)
            return df

    def update_income_statement(self, freq: str = "q"):
        folder = self._get_period_folder(freq)
        path = f"{self.ticker_folder}\\{folder}\\income_statement.csv"
        df = self.scrape_income_statement(freq)
        df.to_csv(path)

    """-----------------------------------"""

    def scrape_balance_sheet(self, freq: str = "q"):
        """
        Scrape the balance sheet table from Stockanalysis.com
        Parameters
        ----------
        ticker : str
           Ticker of the company
        freq : str, optional
            Frequency of data. In Annual(a) or Quarter(q) format, by default "q"

        Returns
        -------
        DataFrame
            Dataframe representing the table scraped.
        """
        if freq in self.annual_params:
            freq = "a"
            url = f"https://stockanalysis.com/stocks/{self.ticker.lower()}/financials/balance-sheet/"
            self.create_browser(url)

        elif freq in self.quarter_params:
            freq = "q"
            url = f"https://stockanalysis.com/stocks/{self.ticker.lower()}/financials/balance-sheet/?p=quarterly"
            self.create_browser(url)
            qtr_button_xpath = xpaths["qtr_button"]
            self.click_button(qtr_button_xpath, wait=True, wait_time=10)
        df = self.get_table(freq=freq, display_dimenstions=True)
        return df

    def get_balance_sheet(self, freq: str = "q"):
        folder = self._get_period_folder(freq)
        path = f"{self.ticker_folder}\\{folder}\\balance_sheet.csv"
        try:
            df = pd.read_csv(path)
            df.rename(columns={"Unnamed: 0": "index"}, inplace=True)
            df.set_index("index", inplace=True)
            return df
        except FileNotFoundError:
            df = self.scrape_balance_sheet(freq)
            df.to_csv(path)
            return df

    def update_balance_sheet(self, freq: str = "q"):
        folder = self._get_period_folder(freq)
        path = f"{self.ticker_folder}\\{folder}\\balance_sheet.csv"
        df = self.scrape_balance_sheet(freq)
        df.to_csv(path)

    """-----------------------------------"""

    def scrape_cash_flow(self, freq: str = "q"):
        """
        Scrape the cash flow table from Stockanalysis.com
        Parameters
        ----------
        ticker : str
           Ticker of the company
        freq : str, optional
            Frequency of data. In Annual(a) or Quarter(q) format, by default "q"

        Returns
        -------
        DataFrame
            Dataframe representing the table scraped.
        """
        if freq in self.annual_params:
            freq = "a"
            url = f"https://stockanalysis.com/stocks/{self.ticker.lower()}/financials/cash-flow-statement/"
            self.create_browser(url)

        elif freq in self.quarter_params:
            freq = "q"
            url = f"https://stockanalysis.com/stocks/{self.ticker.lower()}/financials/cash-flow-statement/?p=quarterly"
            self.create_browser(url)
            qtr_button_xpath = xpaths["qtr_button"]
            self.click_button(qtr_button_xpath, wait=True, wait_time=10)

        df = self.get_table(freq=freq, display_dimenstions=True)
        return df

    def get_cash_flow(self, freq: str = "q"):
        folder = self._get_period_folder(freq)
        path = f"{self.ticker_folder}\\{folder}\\cash_flow.csv"
        try:
            df = pd.read_csv(path)
            df.rename(columns={"Unnamed: 0": "index"}, inplace=True)
            df.set_index("index", inplace=True)
            return df
        except FileNotFoundError:
            df = self.scrape_cash_flow(freq)
            df.to_csv(path)
            return df

    def update_cash_flow(self, freq: str = "q"):
        folder = self._get_period_folder(freq)
        path = f"{self.ticker_folder}\\{folder}\\cash_flow.csv"
        df = self.scrape_cash_flow(freq)
        df.to_csv(path)

    """-----------------------------------"""

    def scrape_ratios(self, freq: str = "q"):
        """
        Scrape the ratios table from Stockanalysis.com
        Parameters
        ----------
        ticker : str
           Ticker of the company
        freq : str, optional
            Frequency of data. In Annual(a) or Quarter(q) format, by default "q"

        Returns
        -------
        DataFrame
            Dataframe representing the table scraped.
        """
        if freq in self.annual_params:
            freq = "a"
            url = f"https://stockanalysis.com/stocks/{self.ticker.lower()}/financials/ratios/"
            self.create_browser(url)
        elif freq in self.quarter_params:
            freq = "q"
            url = f"https://stockanalysis.com/stocks/{self.ticker.lower()}/financials/ratios/?p=quarterly"
            self.create_browser(url)
            qtr_button_xpath = xpaths["qtr_button"]
            self.click_button(qtr_button_xpath, wait=True, wait_time=10)

        df = self.get_table(freq=freq, display_dimenstions=True)
        return df

    def get_ratios(self, freq: str = "q"):
        folder = self._get_period_folder(freq)
        path = f"{self.ticker_folder}\\{folder}\\ratios.csv"
        try:
            df = pd.read_csv(path)
            df.rename(columns={"Unnamed: 0": "index"}, inplace=True)
            df.set_index("index", inplace=True)
            return df
        except FileNotFoundError:
            df = self.scrape_ratios(freq)
            df.to_csv(path)
            return df

    def update_ratios(self, freq: str = "q"):
        folder = self._get_period_folder(freq)
        path = f"{self.ticker_folder}\\{folder}\\ratios.csv"
        df = self.scrape_ratios(freq)
        df.to_csv(path)

    ################################################################### Table Utilities
    def get_table(self, freq: str, display_dimenstions: bool = False):
        """
        Scrapes the elements from table on webpage

        Parameters:
        freq str: Determines if data is in quarterly or annual format.

        Returns:
        Pandas dataframe representing table from webpage.
        """

        dimensions = self.get_table_dimensions(freq=freq)
        row_count = dimensions["row"]
        col_count = dimensions["col"]

        if display_dimenstions:
            print(f"[Table Dimensions]\nRows: {row_count}\nCols: {col_count}")

        row_labels = []
        table_data = {}
        for x in range(row_count):

            row_data = []
            for y in range(col_count):
                # Add 1 to adjust for xpath labels.
                xpath = f"/html/body/div/div[1]/div[2]/main/div[5]/table/tbody/tr[{x+1}]/td[{y+1}]"
                try:
                    data = self.read_data(xpath, wait=True)
                except TimeoutException:
                    data = np.nan

                if self.log_data:
                    print(f"[Data]: {data}")
                if y == 0:
                    row_labels.append(data)
                else:
                    row_data.append(data)
            table_data[row_labels[x]] = row_data
        table_headers = []
        for i in range(col_count):
            xpath = f"/html/body/div/div[1]/div[2]/main/div[5]/table/thead/tr/th[{i+1}]"
            header_data = self.read_data(xpath, wait=True)
            if header_data == "Year" or header_data == "Quarter Ended":
                pass
            else:
                table_headers.append(header_data)
        table_data["Dates"] = table_headers
        df = pd.DataFrame(table_data)
        df.set_index("Dates", inplace=True)
        df = df.T
        df = df.iloc[:, ::-1]

        return df

    def get_table_dimensions(self, freq: str = "q"):
        """
        Counts how many rows and columns are in a table. Will cycle through xpaths if initial attemps are not found.

        Returns:
        Dictionary with keys for row and column
        """

        index = 0
        counting = True
        while counting:
            row_xpath = xpaths["row"][index]
            col_xpath = xpaths["col"][index]
            row_count = self.count_rows(row_xpath, freq=freq, attempt=index)
            col_count = self.count_columns(col_xpath)
            if row_count != 0 and col_count != 0:
                break

            index += 1
        return {"row": row_count, "col": col_count}

    """-----------------------------------"""

    def count_rows(
        self, xpath: str, freq: str, log_xpath: bool = False, attempt: int = 0
    ):
        row_running = True
        row_index = 1
        row_count = 0
        row_labels = []
        if log_xpath:
            print(f"-- [count_rows() Xpath] {xpath}")
        while row_running:
            try:
                if row_index == 1:
                    if freq == "q":
                        _xpath = xpaths["header"][attempt].format(1)
                    elif freq == "a":
                        _xpath = xpaths["header"][attempt].format(1)
                else:
                    _xpath = xpath.format(row_index)

                row_data = self.read_data(_xpath, wait=True, wait_time=10)
                row_count += 1
                row_index += 1
            except NoSuchElementException:
                print(f"[count_rows()] NoSuchElementException")
                row_running = False
            except TimeoutException:
                print(f"[count_rows()] TimeOutException")
                row_running = False

        if row_count == 0:
            print(f"[Warning] 0 rows collected")
        return row_count

    """-----------------------------------"""

    def count_columns(self, xpath: str, log_xpath: bool = False):
        col_running = True
        col_index = 1
        col_count = 0
        if log_xpath:
            print(f"-- [count_columns() Xpath] {xpath}")
        while col_running:
            try:
                _xpath = xpath.format(col_index)
                row_data = self.read_data(_xpath, wait=True, wait_time=10)
                # Exclude premium rows from count.
                if " - " in row_data or "+" in row_data:
                    col_running = False
                    break
                col_count += 1
                col_index += 1
            except NoSuchElementException:
                print(f"[count_columns()] NoSuchElementException")
                col_running = False
            except TimeoutException:
                print(f"[count_columns()] TimeoutException")
                col_running = False

        if col_count == 0:
            print(f"[Warning] 0 columns collected")
        return col_count

    """-----------------------------------"""

    def read_data(self, xpath: str, wait: bool = False, wait_time: int = 5) -> str:
        """
        :param xpath: Path to the web element.
        :param wait: Boolean to determine if selenium should wait until the element is located.
        :param wait_time: Integer that represents how many seconds selenium should wait, if wait is True.
        :return: (str) Text of the element.
        """

        if wait:
            data = WebDriverWait(self.browser, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        else:
            data = self.browser.find_element("xpath", xpath)
        # Return the text of the element found.
        return data.text

    def read_html(self, css_class: str, wait_time: int = 5):
        data = WebDriverWait(self.browser, wait_time).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, css_class))
        )
        return data

    """-------------------------------"""

    def click_button(self, xpath: str, wait: bool = False, wait_time: int = 5) -> None:
        """
        :param xpath: Path to the web element.
        :param wait: Boolean to determine if selenium should wait until the element is located.
        :param wait_time: Integer that represents how many seconds selenium should wait, if wait is True.
        :return: None. Because this function clicks the button but does not return any information about the button or any related web elements.
        """

        if wait:
            element = WebDriverWait(self.browser, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        else:
            element = self.browser.find_element("xpath", xpath)
        element.click()

    """-------------------------------"""

    def halt_scrape(self, func: str):
        print(f"-- [Halted] -- Process stopped within function: {func}.")

    ################################################################### General Utilities
    """-------------------------------"""

    def create_file_path(
        self, ticker: str, base_path: str, freq: str, statement: str
    ) -> str:
        """
        Create a path to csv file based on function parameters.
        """
        if freq in self.quarter_params:
            freq = "Quarter"
        elif freq in self.annual_params:
            freq in "Annual"
        path = f"{base_path}\\EquityData\\Stocks\\{ticker.upper()}\\Statements\\{freq}\\{ticker.upper()}_{statement}.csv"
        return path

    """-------------------------------"""

    def _get_period_folder(self, freq: str):
        if freq in self.annual_params:
            return "Annual"
        elif freq in self.quarter_params:
            return "Quarter"

    """-------------------------------"""

    def _clean_close(self) -> None:
        self.browser.close()
        self.browser.quit()

    """-------------------------------"""
    """-------------------------------"""


if __name__ == "__main__":

    s = StockAnalysis("AAPL")
    df = s.get_cash_flow()
    cols = df.columns.to_list()
    cols = cols[-5:]
    print(f"DF: {df[cols]}")
