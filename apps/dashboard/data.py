import pandas as pd
import numpy as np
from collections import OrderedDict


## For Bar Char
path = "/Users/nickytan/Documents/FS_Data_Science/FusionChartsProject/fusioncharts/utilities/company_list_state_classified.csv"
path2 = "/Users/nickytan/Documents/FS_Data_Science/FusionChartsProject/fusioncharts/utilities/df_companies_state.csv"
df = pd.read_csv(path, index_col=None)

df_companies_state = df.groupby("company_state").agg(
    total_companies=("company_state", "count")).reset_index()


# df_companies_state.to_csv("df_companies_state.csv", index=None)


## For mapn chart
df_companies_state_id = pd.read_csv(path2, index_col=None)

    
df_companies_state_id["id"] = df_companies_state_id["id"].apply(lambda x : "00" + str(x) if x < 10 else "0" + str(x))
df_companies_state_id["total_companies"] = df_companies_state_id["total_companies"].apply(lambda x : str(x))
df_companies_state_id["value_label"] = "1"

x = [id for id in df_companies_state_id["id"]]
x2 =  [value for value in df_companies_state_id["total_companies"]]
x3 = [value for value in df_companies_state_id["value_label"]]

mapDataArray = list(map(list,zip(x,x2,x3)))

print(mapDataArray)