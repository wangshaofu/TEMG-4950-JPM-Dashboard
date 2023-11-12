import pandas as pd
import data_class as dc
import scraper as sc
import warnings
from helper_functions import translate_from_q_to_date

warnings.simplefilter(action='ignore')

if __name__ == '__main__':
    report_quarter = input('Enter period of report(in format of 2023-Q1): ')
    get_date_from_period = translate_from_q_to_date(report_quarter)

    filing = dc.FillingDoc(report_quarter)
    scraper = sc.Scraper()
    scraper.EDGAR_search(report_quarter, filing.get_distinct_accession())
    scraper.preprocess(report_quarter)
