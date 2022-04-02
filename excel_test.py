import pandas as pd

path = "SH_BM_202112.xlsm"

df = pd.read_excel(path, sheet_name="Hoja2")

fila_113 = df.iloc[1]

print(fila_113)