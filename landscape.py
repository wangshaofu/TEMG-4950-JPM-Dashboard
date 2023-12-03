import pandas as pd

def _landscape(prevHoldings,currHoldings,by,n:int=5,inOrOut='I')->pd.DataFrame:
    curr = currHoldings.groupby(level=0)['VALUE'].sum()
    prev = prevHoldings.groupby(level=0)['VALUE'].sum()
    holdingVal = pd.Series(curr,name='Holding Value')
    flow = curr - prev
    if (by=='aum'):
        top = holdingVal
    elif(by=='flow'):
            top = flow
    topInvestors = pd.Series(top.sort_values(ascending=(inOrOut=="O")).head(n=n)/1000000, name='Flow or AUM in $M USD')
    jpmFlow = currHoldings[currHoldings['JPM Product']==True].groupby(level=0)['VALUE'].sum()-prevHoldings[prevHoldings['JPM Product']==True].groupby(level=0)['VALUE'].sum()
    jpmPct = pd.Series((jpmFlow/curr).loc[topInvestors.index].sort_values(ascending=(inOrOut=="O")).fillna(0) *100,name='% JPM Product')
    holdingVal = holdingVal.loc[topInvestors.index]
    return pd.concat([topInvestors,jpmPct,holdingVal/1000000],axis=1)


def landscape(prevHoldings,currHoldings,by,cat='',subCat='',n:int=5,inOrOut='I') -> pd.Series:
    if(bool(cat)&bool(subCat)):
        prevHoldings = prevHoldings[prevHoldings[cat]==subCat]
        currHoldings = currHoldings[currHoldings[cat]==subCat]
    return _landscape(prevHoldings,currHoldings,by,n)

def landscape_issuer(prevHoldings,currHoldings,by,cat='',subCat='',n:int=5,inOrOut='I') -> pd.Series:
    if(bool(cat)&bool(subCat)):
        prevHoldings = prevHoldings[prevHoldings[cat]==subCat]
        currHoldings = currHoldings[currHoldings[cat]==subCat]

    return _landscape_issuer(prevHoldings,currHoldings,by,n)

def _landscape_issuer(prevHoldings,currHoldings,by,n:int=5,inOrOut="I")->pd.DataFrame:
    aum = pd.Series(currHoldings.groupby(level=0)['VALUE'].sum(),name='AUM')
    flow = currHoldings.groupby(level=0)['VALUE'].sum() - prevHoldings.groupby(level=0)['VALUE'].sum()
    aum = aum.drop('Jpmorgan Chase')
    flow = flow.drop('Jpmorgan Chase')

    if (by=='aum'):
        top = aum
    elif(by=='flow'):
        top = flow
    topInvestors = pd.Series(top.sort_values(ascending=(inOrOut=="O")).head(n=n)/1000000, name='Net Flow')
    jpmPct = pd.Series((flow/aum).loc[topInvestors.index].sort_values(ascending=(inOrOut=="O")).fillna(0) *100,name="% Fund Flow / AUM")
    aum = aum.loc[topInvestors.index]
    return pd.concat([topInvestors,jpmPct,aum/1000000],axis=1)
    
def landscape_product(prevHoldings,currHoldings,by,cat='',subCat='',n:int=5,inOrOut='I') -> pd.Series:
    if(bool(cat)&bool(subCat)):
        prevHoldings = prevHoldings[prevHoldings[cat]==subCat]
        currHoldings = currHoldings[currHoldings[cat]==subCat]

    return _landscape_product(prevHoldings,currHoldings,by,n)

def _landscape_product(prevHoldings,currHoldings,by,n:int=5,inOrOut="I")->pd.DataFrame:
    aum = pd.Series(currHoldings.groupby(level=0)['VALUE'].sum(),name='AUM')
    flow = currHoldings.groupby(level=0)['VALUE'].sum() - prevHoldings.groupby(level=0)['VALUE'].sum()
    if (by=='aum'):
        top = aum
    elif(by=='flow'):
        top = flow
    topInvestedProd = pd.Series(top.sort_values(ascending=(inOrOut=="O")).head(n=n)/1000000, name='Net Flow')
    jpmPct = pd.Series((flow/aum).loc[topInvestedProd.index].sort_values(ascending=(inOrOut=="O")).fillna(0) *100,name="% Fund Flow / AUM")
    issuer = pd.Series(currHoldings['Issuer'].loc[topInvestedProd.index],name="Issuer")
    strategy = pd.Series(currHoldings['Strategy'].loc[topInvestedProd.index],name="Strategy")
    aum = aum.loc[topInvestedProd.index]
    return pd.concat([topInvestedProd,jpmPct,aum/1000000,issuer[~issuer.index.duplicated()],strategy[~strategy.index.duplicated()]],axis=1)
    
