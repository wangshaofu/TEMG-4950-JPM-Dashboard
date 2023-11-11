import pandas as pd
import pprint
from helper_functions import translate_from_q_to_date

class FillingDoc:
    def __init__(self, report_quarter):
        self.table_path = f'.\input\{report_quarter}\INFOTABLE.tsv'
        self.table_data = pd.read_csv(self.table_path, sep='\t', header=0)
        self.table_data = self.table_data[
            ['ACCESSION_NUMBER', 'CUSIP', 'VALUE']]

    def show_table(self):
        pprint.pprint(self.table_data)

    def get_distinct_accession(self):
        header = self.table_data[["ACCESSION_NUMBER", "CUSIP"]]
        accession_distinct = header[['ACCESSION_NUMBER']].drop_duplicates()
        return accession_distinct


class CUSIPMapTable:
    def __init__(self):
        self.table_path = f'.\input\CUSIP.csv'
        self.table_data = pd.read_csv(self.table_path, sep=',')
        self.table_data = self.table_data[['Trading Symbol', 'CUSIP']]

    def show_table(self):
        pprint.pprint(self.table_data)


class TickerMeta:
    def __init__(self):
        self.table_path = f'.\input\TickerMeta.csv'
        self.table_data = pd.read_csv(self.table_path, header=0)
        self.table_data = self.table_data[
            ['Trading Symbol', 'ETF Security Description', 'Geography', 'Strategy', 'Sector/Focus', 'Theme', 'Issuer',
             'Asset Class']]


class DTCCode:
    def __init__(self):
        self.table_path = f'.\input\DTCParticipantCode.csv'
        self.table_data = pd.read_csv(self.table_path, sep='\t', header=0)

    def show_table(self):
        pprint.pprint(self.table_data)


class FilingCompanyMap:
    def __init__(self, period_of_report):
        self.table_path = f'.\input\{period_of_report}\FilingNumberMap.csv'
        self.table_data = pd.read_csv(self.table_path, header=0)
        self.table_data = self.table_data[self.table_data['Amend'] == False]
        self.table_data = self.table_data[self.table_data['Period of Report'] == translate_from_q_to_date(period_of_report)]

    def show_table(self):
        pprint.pprint(self.table_data)
