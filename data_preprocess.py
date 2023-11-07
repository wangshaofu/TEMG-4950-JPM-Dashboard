import pandas as pd
import pprint

class FillingDoc:
    def __init__(self):
        self.table_path = f'.\input\INFOTABLE.tsv'
        self.table_data = pd.read_csv(self.table_path, sep='\t', header=0)

    def show_table(self):
        pprint.pprint(self.table_data)

    def get_accession_and_CUSIP(self):
        return self.table_data[["ACCESSION_NUMBER", "CUSIP"]]


class CUSIPMapTable:
    def __init__(self):
        self.table_path = f'.\input\CUSIP.csv'
        self.table_data = pd.read_csv(self.table_path, sep=',')

    def show_table(self):
        pprint.pprint(self.table_data)


class DTCCode:
    def __init__(self):
        self.table_path = f'.\input\DTCParticipantCode.csv'
        self.table_data = pd.read_csv(self.table_path, sep='\t', header=0)

    def show_table(self):
        pprint.pprint(self.table_data)

class FilingCompanyMap:
    def __init__(self):
        self.table_path = f'.\input\FilingNumberMap.csv'
        self.table_data = pd.read_csv(self.table_path, header=0)

    def show_table(self):
        pprint.pprint(self.table_data)