import pandas as pd
import selenium
import data_preprocess as dp
import scraper as sc
import warnings

warnings.simplefilter(action='ignore')

if __name__ == '__main__':
    period_of_report = input('Enter period of report(in format of 2023-06-30): ')
    etf_to_find = input('Enter the specific ETF to find(full list available in CUSIP.csv): ')

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
    # DTC_and_CUSIP_and_company_mapped_table.to_csv(f'.\output\FullTable.csv')
    full_table_only_ETF = DTC_and_CUSIP_and_company_mapped_table[
        DTC_and_CUSIP_and_company_mapped_table['ETF Security Description'].notna()]
    clean_full_table_only_ETF = full_table_only_ETF[
        ['VALUE', 'Company Name', 'Period of Report', 'Amend', 'ETF Security Description', 'ETF Agent',
         'Foreign (F) / Domestic (D)', 'ETF Agent Name']]
    # clean_full_table_only_ETF.to_csv(f'.\output\CleanETFTable.csv')
    clean_full_table_only_ETF['ETF_target?'] = list(
        # map(lambda x: x.startswith(('JP', 'J P')), clean_full_table_only_ETF['ETF Security Description']))
        map(lambda x: x.startswith(etf_to_find), clean_full_table_only_ETF['ETF Security Description']))
    clean_full_table_only_ETF = clean_full_table_only_ETF[
        (clean_full_table_only_ETF['ETF_target?']) & (clean_full_table_only_ETF['Period of Report'] == period_of_report)]
    print(clean_full_table_only_ETF)
    clean_full_table_only_ETF.to_csv(f'.\output\CleanETFTableOnly{etf_to_find}.csv')
    # check if have amend and non amend exist at the same time
    grouped = clean_full_table_only_ETF.groupby(['Company Name', 'Amend'])
    company_names = grouped.groups.keys()
    print(company_names)
    # filtered_company_names = [name[0] for name in company_names if (True in name) and (False in name)]
    # print(filtered_company_names)
    sum_by_company = clean_full_table_only_ETF.groupby('Company Name')['VALUE'].sum().reset_index().sort_values('VALUE',
                                                                                                                ascending=False)
    total_value = sum_by_company['VALUE'].sum()

    # Create a new DataFrame with the total value in the first row
    total_value_row = pd.DataFrame({'Company Name': ['Total Value'], 'VALUE': [total_value]})
    output_data = pd.concat([total_value_row, sum_by_company])
    output_data.to_csv(f'.\output\specific_etf\{etf_to_find}TopHoldingCompanyValue.csv')

    # print(clean_full_table_only_ETF.isnull().sum())
