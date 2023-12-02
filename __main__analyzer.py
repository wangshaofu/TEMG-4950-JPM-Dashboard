import pandas as pd
from helper_functions import translate_from_q_to_date


def filter_function(mode, query, report_quarter):
    full_filing_info_table = pd.read_csv(f'.\output\{report_quarter}\FullETFTable.csv')
    specific_table = None
    if mode == 'ETF':
        # find the specific ETF
        specific_table = full_filing_info_table[full_filing_info_table['ETF Security Description'] == query]
    elif mode == 'Issuer':
        # find the specific issuer
        specific_table = full_filing_info_table[(full_filing_info_table['Issuer'] == query)]
    elif mode == 'Asset Class':
        specific_table = full_filing_info_table[full_filing_info_table['Asset Class'] == query]
    sum_by_company = specific_table.groupby('Company Name')['VALUE'].sum().reset_index().sort_values('VALUE',
                                                                                                     ascending=False)
    total_value = sum_by_company['VALUE'].sum()
    total_value_row = pd.DataFrame({'Company Name': ['Total Value'], 'VALUE': [total_value]})
    output_data = pd.concat([total_value_row, sum_by_company])
    output_data.to_csv(f'.\output\query_output\{query}_{report_quarter}.csv')


if __name__ == '__main__':
    report_quarter = input('Enter period of report(in format of 2023-Q1): ')
    get_date_from_period = translate_from_q_to_date(report_quarter)
    search_mode = input('Enter search mode(1 for specific ETF, 2 for specific issuer, 4 for asset class): ')
    print('The query `full list available in TickerMeta.csv')
    if search_mode == '1':
        mode = 'ETF'
        query = input('Enter the specific ETF Security Description: ')
    elif search_mode == '2':
        mode = 'Issuer'
        query = input('Enter the specific Issuer to find(full list available in TickerMeta.csv): ')
    elif search_mode == '3':
        mode = 'Asset Class'
        query = input('Enter the specific Asset Class to find: ')
    else:
        print('Bad search mode')
        exit(0)
    filter_function(mode=mode, query=query, report_quarter=report_quarter)
