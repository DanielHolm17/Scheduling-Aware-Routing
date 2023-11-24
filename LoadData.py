import pandas as pd
import os

# /Users/mathiasmagnusson/Zone-routing-protocol/data.csv

#FILE_PATH = os.environ.get("/Users/mathiasmagnusson/Zone-routing-protocol/data.csv")

headers = [f"sat{i}" for i in range(0, 66)]
data = pd.read_csv("Scheduling-Aware-Routing/data.csv", names=headers)


def get_position_data(satIndex: int):
    return data.iloc[:,satIndex]
