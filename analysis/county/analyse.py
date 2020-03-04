import pandas as pd
import sklearn.metrics as sklm
import scipy.stats as ss
from math import sqrt


def new_r2(x, model, gmfd, usda):
    return sklm.r2_score(x[gmfd * 'GMFD' + usda * 'USDA'], x[model])


def new_mse(x, model, gmfd, usda):
    return sklm.mean_squared_error(x[gmfd * 'GMFD' + usda * 'USDA'], x[model])


def new_rmse(x, model, gmfd, usda):
    return sqrt(sklm.mean_squared_error(x[gmfd * 'GMFD' + usda * 'USDA'], x[model]))


def new_mae(x, model, gmfd, usda):
    return sklm.median_absolute_error(x[gmfd * 'GMFD' + usda * 'USDA'], x[model])


def new_pearson(x, model, gmfd, usda):
    return ss.pearsonr(x[gmfd * 'GMFD' + usda * 'USDA'], x[model])[0]


def new_spearman(x, model, gmfd, usda):
    return ss.spearmanr(x[gmfd * 'GMFD' + usda * 'USDA'], x[model])[0]


def AgVarVerify(data, metric, yearMin=1956, yearMax=2005, plot=False):
    """
    Calculate verification metrics of each ensemble member against GMFD truth

    Inputs:
        - data : Pandas DataFrame with models in columns and a 'GMFD' columns
        - metric : Verification metric to be calculated. Choose from:
                    pearson, spearman, mse, mae, r2, sdR, madR
        - yearMin : First year of sample, defaults to earliest common year
        - yearMax : Last year of sample, defaults to latest common year
    """
    # Set correct GEOID structure, filter by years
    data["GEOID"] = data["GEOID"].astype(str).str.zfill(5)
    data = data.query('Year >= ' + str(yearMin) + ' and Year <= ' + str(yearMax))
    # Set correct indexing structure
    data.set_index(["AgVar", "GEOID"], inplace=True)
    # Drop NaNs - Check this!!!
    data = data.drop(columns='Year').dropna()
    # Each DataSeries will be appended to 'res'
    res = []
    # Set correct grouping
    dataGrouped = data.groupby(['AgVar', 'GEOID'])
    # Read verification metric and assign correct 'myfunc'
    myfunc = globals()['new_' + metric]
    # Calculate verification metric
    for model_name in data.columns[:-1]:
        res.append(dataGrouped.apply(myfunc, model_name, True, False))
    # Return DataFrame of metric for each model and GEOID
    return pd.DataFrame(res, index=data.columns[:-1]).T


def YieldVerify(data, metric, yearMin=1950, yearMax=2005, min=40, gmfd=False, usda=True):
    """
    Calculate verification metrics of each ensemble member against GMFD or USDA truth

    Inputs:
        - data : Pandas DataFrame with models in columns and a 'GMFD' columns
        - metric : Verification metric to be calculated. Choose from:
                    pearson, spearman, mse, mae, r2, sdR, madR
        - yearMin : First year of sample, defaults to earliest common year
        - yearMax : Last year of sample, defaults to latest common year
        - min: Minimum number of GMFD/USDA years required to calculate statistics
        - gmfd/usda : Dataset to verify against
    """
    # Set correct default for GMFD start year
    if gmfd and yearMin != 1950:
        yearMin = 1960
    # Set correct GEOID structure, filter by years
    data["GEOID"] = data["GEOID"].astype(str).str.zfill(5)
    data = data.query('Year >= ' + str(yearMin) + ' and Year <= ' + str(yearMax))
    # Set correct indexing structure
    if gmfd:
        data.set_index(['AgVar', 'GEOID'], inplace=True)
    elif usda:
        data.set_index(['GEOID'], inplace=True)
    # Drop GEOIDS with too few observations
    bad = data['USDA'].isna().sum(level='GEOID') > (yearMax - yearMin - min)
    data = data.drop(bad[bad == True].index)
    # Drop NaNs - Check this!!!
    data = data.drop(columns='Year').dropna()
    # Each DataSeries will be appended to 'res'
    res = []
    # Set correct grouping
    if gmfd:
        dataGrouped = data.groupby(['AgVar', 'GEOID'])
    elif usda:
        dataGrouped = data.groupby(['GEOID'])
    # Read verification metric and assign correct 'myfunc'
    myfunc = globals()['new_' + metric]
    # Calculate verification metric
    if gmfd:
        models = data.columns.drop(['GMFD', 'USDA'])
    elif usda:
        models = data.columns.drop(['USDA'])
    for model_name in models:
        res.append(dataGrouped.apply(myfunc, model_name, gmfd, usda))
    # Return DataFrame of metric for each model and GEOID
    return pd.DataFrame(res, index=models).T


def Ratio(nex, cmip):
    """
    Calculates the ratio of two verification metrics for each model (NEX/CMIP)

    Inputs:
        nex: NEX DataFrame
        cmip: CMIP DataFrame
    """
    # Merge
    if 'AgVar' in nex.reset_index().columns:
        data = pd.merge(nex, cmip, on=['AgVar', 'GEOID'], how='inner', suffixes=['_nex', '_cmip'])
    else:
        data = pd.merge(nex, cmip, on=['GEOID'], how='inner', suffixes=['_nex', '_cmip'])
    # Calculate ratios
    for model in nex.columns:
        data[model] = data[model + '_nex'] / data[model + '_cmip']
        data.drop(columns=[model + '_nex', model + '_cmip'], inplace=True)
    # Return new DataFrame
    return data
