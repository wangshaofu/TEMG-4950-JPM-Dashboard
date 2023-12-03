import pandas as pd

def portfolio(prev,curr,cat,subCat)->list[int]: 
    if(bool(cat)&bool(subCat)):  
        prev = prev[prev[cat]==subCat]
        curr = curr[curr[cat]==subCat]
    return [prev['TOTAL VALUE'][0],curr['TOTAL VALUE'][0],curr['TOTAL VALUE'][0]-prev['TOTAL VALUE'][0]]    

def holding_change(prevHoldings,currHoldings,by,n:int=5,cat='',subCat='',inOrOut='I')->pd.DataFrame:
    if(bool(cat)&bool(subCat)):
        prevHoldings = prevHoldings[prevHoldings[cat]==subCat]
        currHoldings = currHoldings[currHoldings[cat]==subCat]
    return _holding_change(prevHoldings,currHoldings,by,n,inOrOut)

def _holding_change(prevHoldings,currHoldings,by,n:int=5,inOrOut="I")->pd.DataFrame:
    curr =  pd.Series(currHoldings.groupby('ETF Security Description')['VALUE'].sum(),name='Holdings')
    netflow = currHoldings.groupby('ETF Security Description')['VALUE'].sum() - prevHoldings.groupby('ETF Security Description')['VALUE'].sum()
    if (by=='aum'):
        top = curr
    elif (by=='flow'):
        top = netflow
    topProd = pd.Series((top).sort_values(ascending=(inOrOut=="O")).fillna(0).head(n=n)/1000000,name='Net Flow or AUM in $M USD')
    topProdPct =  pd.Series(((netflow)/curr).loc[topProd.index] *100,name='% Flow / AUM' )
    ETFlist = currHoldings[currHoldings['ETF Security Description'].isin(topProd.index)].set_index("ETF Security Description",drop=True)
    issuer = pd.Series(ETFlist['Issuer'],name="Issuer")
    strategy = pd.Series(ETFlist['Strategy'],name="Strategy")
    geography = pd.Series(ETFlist['Geography'],name="Geography")
    return pd.concat([topProd,topProdPct,curr.loc[topProd.index]/1000000,issuer[~issuer.index.duplicated()],strategy[~strategy.index.duplicated()],geography[~geography.index.duplicated()]],axis=1)