import pandas as pd

path = "SH_BM_202112.xlsm"

df = pd.read_excel(path, sheet_name="Hoja2", )

print(df.columns)
