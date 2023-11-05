import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd



class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.reportdf = pd.DataFrame(columns=['ACCESSION_NUMBER', 'Company Name', 'Period of Report', 'Amend'])

    def EDGAR_search(self, accession_distinct):
        # target_address = f"https://www.sec.gov/Archives/edgar/data/1092838/000109283823000009/0001092838-23-000009-index.html"
        # 0000922423-23-000066 fails
        for index, row in accession_distinct.iterrows():
            amend_check = None
            target_address = f"https://www.sec.gov/Archives/edgar/data/{row['ACCESSION_NUMBER'][3:10]}/{row['ACCESSION_NUMBER'].replace('-', '')}/{row['ACCESSION_NUMBER']}-index.html"
            self.driver.get(target_address)
            try:
                company_info = self.driver.find_element('xpath', '//span[@class="companyName"]').text
                company_name = company_info.split("(")[0].strip()
                period_of_report = self.driver.find_element('xpath',
                                                            '//div[@class="formGrouping"]/div[@class="infoHead"][text('
                                                            ')="Period of Report"]/following-sibling::div['
                                                            '@class="info"]').text
                form_name = self.driver.find_element('id', 'formName').text
                if '[Amend]' in form_name:
                    amend_check = True  # is amend
                else:
                    amend_check = False
            except NoSuchElementException:
                company_name = None
                period_of_report = None
                amend_check = None
            self.reportdf = self.reportdf.append({'ACCESSION_NUMBER': row['ACCESSION_NUMBER'],
                                                  'Company Name': company_name,
                                                  'Period of Report': period_of_report,
                                                  'Amend': amend_check}, ignore_index=True)
            print(len(self.reportdf))
            print(row['ACCESSION_NUMBER'], company_name, period_of_report, amend_check)
        self.reportdf.to_csv(f".\FilingNumberMap.csv",index=False)
        # last_company_name = None
        # company_name = None
        # for index, row in accession_distinct.iterrows():
        #     accession_number = row['ACCESSION_NUMBER']
        #     target_address = f'https://www.sec.gov/edgar/search/#/q={accession_number}&dateRange=1y&category=custom&forms=13F-HR'
        #     while company_name == last_company_name or company_name is None:
        #         try:
        #             print("running here")
        #             self.driver.get(target_address)
        #             company_name = self.driver.find_element('xpath', '//td[@class="entity-name"]').text
        #             print("last company:", last_company_name)
        #             print("this company:", company_name)
        #             time.sleep(1)
        #             self.driver.refresh()
        #         except NoSuchElementException:
        #             # stupid SEC
        #             self.driver.refresh()
        #             continue
        #
        #     print("ACCESSION_NUMBER",  accession_number, "maps to", company_name)
        #     last_company_name = company_name
        #     time.sleep(3)
