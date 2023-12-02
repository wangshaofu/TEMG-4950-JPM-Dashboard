import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import data_class as dc
from helper_functions import translate_from_q_to_date


class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.reportdf = pd.DataFrame(columns=['ACCESSION_NUMBER', 'Company Name', 'Period of Report', 'Amend'])

    def EDGAR_search(self, report_quarter, accession_distinct):
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
        self.reportdf.to_csv(f".\input\{report_quarter}\FilingNumberMap.csv", index=False)
        self.driver.close()
    def preprocess(self, report_quarter):
        filing = dc.FillingDoc(report_quarter)
        CUSIP_map = dc.CUSIPMapTable()
        ticker_meta = dc.TickerMeta()
        filing_company_map = dc.FilingCompanyMap(report_quarter)
        full_filing_info_table = filing.table_data.merge(filing_company_map.table_data, on='ACCESSION_NUMBER',
                                                         how='left').dropna(subset=['Company Name'])
        full_filing_info_table = full_filing_info_table.merge(CUSIP_map.table_data, on='CUSIP', how='left')
        full_filing_info_table = full_filing_info_table.merge(ticker_meta.table_data, on='Trading Symbol', how='inner')
        # This output csv should be every filing containing etf with non-amend filing
        full_filing_info_table.to_csv(f'.\output\{report_quarter}\FullETFTable.csv')
