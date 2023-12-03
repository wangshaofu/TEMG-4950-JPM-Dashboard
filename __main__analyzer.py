import pandas as pd
import warnings
from landscape import landscape, landscape_issuer, landscape_product
from investor import portfolio, holding_change
from competitor import aum, top_bear
# Ignore warnings
warnings.filterwarnings('ignore')
# Load various data files
cleanETFtable = pd.read_csv("./CleanETFTableUpdated.csv")
fundValue = pd.read_csv("./JPMValue.csv")
cleanETFtable = cleanETFtable.drop(['Unnamed: 0'],axis=1)

# extract the companies who filed for amended reports 
filingPeriodList = cleanETFtable['Period of Report'].unique() 
lastTwoFiling = filingPeriodList[:2]
cleanETFtable = cleanETFtable[cleanETFtable['Period of Report'].isin(lastTwoFiling)]# comment this if u want all filings 
CompanyReviewList = set(cleanETFtable[cleanETFtable['Period of Report']==lastTwoFiling[0]]['Company Name']).intersection(set(cleanETFtable[cleanETFtable['Period of Report']==lastTwoFiling[1]]['Company Name']))
cleanETFtableCompare = cleanETFtable[cleanETFtable['Company Name'].isin(list(CompanyReviewList))]

#transform the dataset for client / competitor analysis
multiClient = cleanETFtableCompare.set_index(['Company Name',
                                              'Period of Report',
                                              'Issuer'

],drop=False)
multiClient2 = cleanETFtableCompare.set_index([
                                              'Period of Report',
                                              'Company Name',
                                              'Issuer',

],drop=False)

#product level query
multiCompetitor = cleanETFtableCompare.set_index([
                                              'Period of Report',
                                              'ETF Security Description',
                                              ],drop=False)
#competitor-client query
multiCompetitor2 = cleanETFtableCompare.set_index([
                                              'Period of Report',
                                              'Issuer'
                                              ],drop=True)
multiCompetitor3  = cleanETFtableCompare.set_index([
                                              'Issuer',
                                              'Period of Report',
                                              'ETF Security Description',
                                              'Company Name',
                                              ],drop=False)

if __name__ == "__main__":
    while(True):
        option = input("Enter Commands for analysis. L for ETF Landscape, I for Investor Tracker and C for Competitor Tracker.: ")
        cat = input("Input the market category (Asset Class, Strategy...) ,empty for default view: ")
        if(cat):
            subCat = input("Input the market subcategory, empty for default view: ")
        else:
            subCat = ''
        n = input("Number of companies / ETF Products to evaluate and show (default 5): ")
        if(n):
            n=int(n)
        else:
            n=5
        by = input("Ranking Method {flow,aum}, default flow: ")
        if(not by):
           by='flow'
        inOrOut = input("Track Top Inflow or Outflow,default inflow: (I/O)")
        if(not inOrOut):
            inOrOut='I'
        if(option=='L'):

            if(subCat):
                print(f"Top Investors of {subCat}")
            else:
                print("Top Investors")
            print(landscape(multiClient2.loc[lastTwoFiling[1]],multiClient2.loc[lastTwoFiling[0]],cat=cat,subCat=subCat,by=by,n=n,inOrOut=inOrOut))
            print("")
            print("Top Competitors")
            print(landscape_issuer(multiCompetitor2.loc[lastTwoFiling[1]],multiCompetitor2.loc[lastTwoFiling[0]],cat=cat,subCat=subCat,by=by,n=n,inOrOut=inOrOut))
            print("")            
            print("Top Products")
            print(landscape_product(multiCompetitor.loc[lastTwoFiling[1]],multiCompetitor.loc[lastTwoFiling[0]],cat=cat,subCat=subCat,by=by,n=n,inOrOut=inOrOut))
        elif (option=='I'):
            investor = input("Investor to be tracked (L for the list of all investors available): ")
            if (investor == "L"):
                print(CompanyReviewList)
                investor = input("Investor to be tracked: ")

            investorPort = multiClient.loc[investor]
            portVal = portfolio(investorPort.loc[lastTwoFiling[1]],investorPort.loc[lastTwoFiling[0]],cat=cat,subCat=subCat)
            print(f"Investor {investor}")
            print(f"Previous Holding: {portVal[0]}")
            print(f"New Holding: {portVal[1]}")
            print(f"Net Inflow(Outflow) to Holding: {portVal[2]}")
            print("")
            print("Top Products:")
            print(holding_change(investorPort.loc[lastTwoFiling[1]],investorPort.loc[lastTwoFiling[0]],by=by,n=n,inOrOut=inOrOut))

        elif (option=='C'):
            issuer = input("Issuer to be tracked (L for the list of all Issuers available): ")
            if (issuer == "L"):
                print(cleanETFtableCompare['Issuer'].unique())
                issuer = input("Issuer to be tracked: ")
            issuerProd = multiCompetitor3.loc[issuer]
            prodVal = aum(issuerProd.loc[lastTwoFiling[1]],issuerProd.loc[lastTwoFiling[0]],cat=cat,subCat=subCat)
            print(f"Investor {issuer}")
            print(f"Previous AUM: {prodVal[0]}")
            print(f"New AUM: {prodVal[1]}")
            print(f"Net Inflow(Outflow) to Products: {prodVal[2]}")
            print("")
            print("Top Investor-Product:")
            print(top_bear(issuerProd.loc[lastTwoFiling[1]],issuerProd.loc[lastTwoFiling[0]],n=n,inOrOut=inOrOut))