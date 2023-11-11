def translate_from_q_to_date(period_of_report):
    year = period_of_report.split('-')[0]
    quarter = period_of_report.split('-')[1]
    if quarter == 'Q1':
        return f'{year}-03-31'
    elif quarter == 'Q2':
        return f'{year}-06-30'
    elif quarter == 'Q3':
        return f'{year}-09-30'
    elif quarter == 'Q4':
        return f'{year}-12-31'
    else:
        print('Error: Invalid period of report')
        return None
