import numpy as np
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


def new_mdae(x, model, gmfd, usda):
    return sklm.median_absolute_error(x[gmfd * 'GMFD' + usda * 'USDA'], x[model])


def new_mae(x, model, gmfd, usda):
    return sklm.mean_absolute_error(x[gmfd * 'GMFD' + usda * 'USDA'], x[model])


def new_pearson(x, model, gmfd, usda):
    return ss.pearsonr(x[gmfd * 'GMFD' + usda * 'USDA'], x[model])[0]


def new_spearman(x, model, gmfd, usda):
    return ss.spearmanr(x[gmfd * 'GMFD' + usda * 'USDA'], x[model])[0]


def new_sdratio(x, model, gmfd, usda):
    return np.std(x[model]) / np.std(x[gmfd * 'GMFD' + usda * 'USDA'])


def spr_var(x, model):
    return np.var(x[model])


def new_madratio(x, model, gmfd, usda):
    return ss.median_absolute_deviation(x[model]) / ss.median_absolute_deviation(x[gmfd * 'GMFD' + usda * 'USDA'])


def make_sa(data):
    return (data - data.mean())/np.std(data)


def AgVarVerify(data, metric, yearMin=1956, yearMax=2005):
    """
    Calculate verification metrics of each ensemble member against GMFD truth

    Inputs:
        - data : Pandas DataFrame with models in columns and a 'GMFD' columns
        - metric : Verification metric to be calculated.
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


def AgVarSPR(data, yearMin=1956, yearMax=2005):
    """
    Calculate spread-skill ratio of ensemble whole against GMFD truth

    Inputs:
        - data : Pandas DataFrame with models in columns and a 'GMFD' columns
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
    # Calculate STDs
    for model_name in data.columns[:-1]:
        if model_name == 'ensemble_mean':
            res.append(dataGrouped.apply(new_rmse, model_name, True, False))
        else:
            res.append(dataGrouped.apply(spr_var, model_name))
    # Set DataFrame of SPR for each model and GEOID
    res = pd.DataFrame(res, index=data.columns[:-1]).T
    # Get means of STD
    std = res.drop(columns = ['ensemble_mean']).mean(axis = 1)
    # Get RMSE of ensemble_mean
    rmse = res.filter(['ensemble_mean'])
    # Merge again
    final = pd.merge(rmse, pd.DataFrame(std, index = std.index, columns = ['var']), on = ['AgVar', 'GEOID'])
    # Return final
    final['SPR'] = np.sqrt(final['var']) / final['ensemble_mean']
    return final.drop(columns = ['var', 'ensemble_mean'])


def AgVarCRPS(data, yearMin=1956, yearMax=2005):
    """
    Calculate Continuous Rank Probability Score of ensemble whole against GMFD truth

    Inputs:
        - data : Pandas DataFrame with models in columns and a 'GMFD' columns
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
    # Calculate STDs
    for model_name in data.columns[:-2]:
        if model_name == 'ensemble_mean':
            res.append(dataGrouped.apply(new_rmse, model_name, True, False))
        else:
            res.append(dataGrouped.apply(spr_var, model_name))
    # Set DataFrame of SPR for each model and GEOID
    res = pd.DataFrame(res, index=data.columns[:-1]).T
    # Get means of STD
    std = res.drop(columns = ['ensemble_mean']).mean(axis = 1)
    # Get RMSE of ensemble_mean
    rmse = res.filter(['ensemble_mean'])
    # Merge again
    final = pd.merge(rmse, pd.DataFrame(std, index = std.index, columns = ['var']), on = ['AgVar', 'GEOID'])
    # Return final
    final['SPR'] = np.sqrt(final['var']) / final['ensemble_mean']
    return final.drop(columns = ['var', 'ensemble_mean'])


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
    if gmfd and yearMin == 1950:
        yearMin = 1956
    # Set correct GEOID structure, filter by years
    data["GEOID"] = data["GEOID"].astype(str).str.zfill(5)
    data = data.query('Year >= ' + str(yearMin) + ' and Year <= ' + str(yearMax))
    # Set correct indexing structure
    data.set_index(['GEOID'], inplace=True)
    # Drop GEOIDS with too few observations
    bad = data[usda*'USDA' + gmfd*'GMFD'].isna().sum(level='GEOID') > (yearMax - yearMin - min)
    data = data.drop(bad[bad == True].index)
    # Drop NaNs - Check this!!!
    if usda:
        data = data.drop(columns='Year').dropna()
    elif gmfd:
        data = data.drop(columns='Year')
    # Each DataSeries will be appended to 'res'
    res = []
    # Set correct grouping
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


def YieldSPR(data, yearMin=1950, yearMax=2005, min=40, gmfd=False, usda=True):
    """
    Calculate spread-skill ratio for whole ensemble against GMFD or USDA truth

    Inputs:
        - data : Pandas DataFrame with models in columns and a 'GMFD' columns
        - yearMin : First year of sample, defaults to earliest common year
        - yearMax : Last year of sample, defaults to latest common year
        - min: Minimum number of GMFD/USDA years required to calculate statistics
        - gmfd/usda : Dataset to verify against
    """
    # Set correct default for GMFD start year
    if gmfd and yearMin != 1950:
        yearMin = 1956
    # Set correct GEOID structure, filter by years
    data["GEOID"] = data["GEOID"].astype(str).str.zfill(5)
    data = data.query('Year >= ' + str(yearMin) + ' and Year <= ' + str(yearMax))
    # Set correct indexing structure
    if gmfd:
        data.set_index(['GEOID'], inplace=True)
    elif usda:
        data.set_index(['GEOID'], inplace=True)
    # Drop GEOIDS with too few observations
    bad = data[usda*'USDA' + gmfd*'GMFD'].isna().sum(level='GEOID') > (yearMax - yearMin - min)
    data = data.drop(bad[bad == True].index)
    # Drop NaNs - Check this!!!
    data = data.drop(columns='Year').dropna()
    # Each DataSeries will be appended to 'res'
    res = []
    # Set correct grouping
    if gmfd:
        dataGrouped = data.groupby(['GEOID'])
    elif usda:
        dataGrouped = data.groupby(['GEOID'])
    # Calculate verification metric
    if gmfd:
        models = data.columns.drop(['GMFD', 'USDA'])
    elif usda:
        models = data.columns.drop(['USDA'])
   # Calculate STDs
    for model_name in data.columns[:-1]:
        if model_name == 'ensemble_mean':
            res.append(dataGrouped.apply(new_rmse, model_name, gmfd, usda))
        else:
            res.append(dataGrouped.apply(spr_var, model_name))
    # Set DataFrame of SPR for each model and GEOID
    res = pd.DataFrame(res, index=data.columns[:-1]).T
    # Get means of STD
    std = res.drop(columns = ['ensemble_mean']).mean(axis = 1)
    # Get RMSE of ensemble_mean
    rmse = res.filter(['ensemble_mean'])
    # Merge again
    final = pd.merge(rmse, pd.DataFrame(std, index = std.index, columns = ['var']), on = ['GEOID'])
    # Return final
    final['SPR'] = np.sqrt(final['var']) / final['ensemble_mean']
    return final.drop(columns = ['var', 'ensemble_mean'])


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
        data.set_index(['AgVar', 'GEOID'], inplace = True)
    else:
        data = pd.merge(nex, cmip, on=['GEOID'], how='inner', suffixes=['_nex', '_cmip'])
        data.set_index(['GEOID'], inplace = True)
    # Calculate ratios
    for model in nex.columns:
        data[model] = data[model + '_nex'] / data[model + '_cmip']
        data.drop(columns=[model + '_nex', model + '_cmip'], inplace=True)
    # Return new DataFrame
    return data
