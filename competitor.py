import pandas as pd

def aum(prev,curr,cat,subCat)->list[int]:   
    if(bool(cat)&bool(subCat)):
        prev = prev[prev[cat]==subCat]
        curr = curr[curr[cat]==subCat] 
    return [prev['TOTAL VALUE'][0],curr['TOTAL VALUE'][0],curr['TOTAL VALUE'][0]-prev['TOTAL VALUE'][0]]    

def top_bear(prevHoldings,currHoldings,n:int=5,cat='',subCat='',inOrOut='I')->pd.DataFrame:
    if(bool(cat)&bool(subCat)):
        prevHoldings = prevHoldings[prevHoldings[cat]==subCat]
        currHoldings = currHoldings[currHoldings[cat]==subCat]
    return _top_bear(prevHoldings,currHoldings,n,inOrOut)

def _top_bear(prevHoldings,currHoldings,n:int=5,inOrOut="I")->pd.DataFrame:
    curr =  pd.Series(currHoldings.groupby(level=[0,1])['VALUE'].sum(),name='Holdings')
    netflow = currHoldings.groupby(level=[0,1])['VALUE'].sum() - prevHoldings.groupby(level=[0,1])['VALUE'].sum()

    topBear = pd.Series((netflow).sort_values(ascending=(inOrOut=="O")).fillna(0).head(n=n)/1000000,name='Net Flow in $M USD')
    topBearPct =  pd.Series(((netflow)/curr).loc[topBear.index] *100,name='% Flow / AUM' )
    ETFlist = currHoldings.loc[topBear.index]
    issuer = pd.Series(ETFlist['Issuer'],name="Issuer")
    strategy = pd.Series(ETFlist['Strategy'],name="Strategy")
    geography = pd.Series(ETFlist['Geography'],name="Geography")
    return pd.concat([topBear,topBearPct,curr.loc[topBear.index]/1000000,issuer[~issuer.index.duplicated()],strategy[~strategy.index.duplicated()],geography[~geography.index.duplicated()]],axis=1)