import pandas as pd

df = pd.read_csv("data/contrataciones.csv")
df = df.sort_values(by=["año", "mes", "rubro", "cuil"])
df.to_parquet("data/contrataciones.parquet.brotli", compression="brotli")
