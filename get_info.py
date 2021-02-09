import os
import pandas as pd

for dataset in os.listdir("newdata"):
    print(dataset)
    df = pd.read_csv(os.path.join("newdata", dataset))
    print(df.describe())