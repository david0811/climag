import numpy as np
import pandas as pd
# import geopandas as gp
# import earthpy.clip as ec
import matplotlib.pyplot as plt

import sklearn.metrics as sklm
import scipy.stats as ss


def new_r2(x, model, gmfd, usda):
    return sklm.r2_score(x[gmfd * 'GMFD' + usda * 'USDA'], x[model])


def new_mse(x, model, gmfd, usda):
    return sklm.mean_squared_error(x[gmfd * 'GMFD' + usda * 'USDA'], x[model])


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
    data["GEOID"] = data["GEOID"].astype(str).str.zfill(5)
    data = data.query('Year >= ' + str(yearMin) + ' and Year <= ' + str(yearMax))
    data.set_index(["AgVar", "GEOID"], inplace=True)
    data.drop(columns='Year', inplace=True)
    data = data.dropna()  # Check this!!

    res = []
    dataGrouped = data.groupby(['AgVar', 'GEOID'])
    myfunc = globals()['new_' + metric]
    for model_name in data.columns[:-1]:
        res.append(dataGrouped.apply(myfunc, model_name, True, False))

    return pd.DataFrame(res, index=data.columns[:-1]).T
