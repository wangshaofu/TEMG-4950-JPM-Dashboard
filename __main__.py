import pandas as pd
import selenium
import data_preprocess as dp
import scraper as sc
import warnings

warnings.simplefilter(action='ignore')

if __name__ == '__main__':
    filing = dp.FillingDoc()
    filing.show_table()
    CUSIP_map = dp.CUSIPMapTable()
    CUSIP_map.show_table()
    DTC_code = dp.DTCCode()
    DTC_code.show_table()
    filing_company_map = dp.FilingCompanyMap()
    filing_company_map.show_table()
    # print(filing_company_map)
    # DTC_code.show_table()
    # header = filing.get_accession_and_CUSIP()
    # accession_distinct = header[['ACCESSION_NUMBER']].drop_duplicates()
    # print(accession_distinct)
    # scraper = sc.Scraper()
    # scraper.EDGAR_search(accession_distinct)
    # print(accession_distinct)
    company_mapped_table = filing.table_data.merge(filing_company_map.table_data, on='ACCESSION_NUMBER', how='left')
    # print(company_mapped_table)
    CUSIP_and_company_mapped_table = company_mapped_table.merge(CUSIP_map.table_data, on='CUSIP', how='left')

    DTC_and_CUSIP_and_company_mapped_table = CUSIP_and_company_mapped_table.merge(DTC_code.table_data, on='ETF Agent',
                                                                                  how='left')
    DTC_and_CUSIP_and_company_mapped_table.to_csv(f'.\FullTable.csv')
    full_table_only_ETF = DTC_and_CUSIP_and_company_mapped_table[
        DTC_and_CUSIP_and_company_mapped_table['ETF Security Description'].notna()]
    clean_full_table_only_ETF = full_table_only_ETF[
        ['VALUE', 'Company Name', 'Period of Report', 'Amend', 'ETF Security Description', 'ETF Agent',
         'Foreign (F) / Domestic (D)', 'ETF Agent Name']]
    clean_full_table_only_ETF.to_csv(f'.\CleanETFTable.csv')
    clean_full_table_only_ETF['JPM?'] = list(
        map(lambda x: x.startswith(('JP', 'J P')), clean_full_table_only_ETF['ETF Security Description']))
    clean_full_table_only_ETF = clean_full_table_only_ETF[
        (clean_full_table_only_ETF['JPM?']) & (clean_full_table_only_ETF['Period of Report'] == '2023-06-30')]
    print(clean_full_table_only_ETF)
    clean_full_table_only_ETF.to_csv(f'.\CleanETFTableOnlyJPM.csv')
    # check if have amend and non amend exist at the same time
    grouped = clean_full_table_only_ETF.groupby(['Company Name', 'Amend'])
    company_names = grouped.groups.keys()
    print(company_names)
    filtered_company_names = [name[0] for name in company_names if (True in name) and (False in name)]
    print(filtered_company_names)
    sum_by_company = clean_full_table_only_ETF.groupby('Company Name')['VALUE'].sum().reset_index().sort_values('VALUE',
                                                                                                                ascending=False)
    print(sum_by_company)
    sum_by_company.to_csv(f'.\JPMValue.csv')

    # print(clean_full_table_only_ETF.isnull().sum())
