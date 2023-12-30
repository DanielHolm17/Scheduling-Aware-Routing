import pandas as pd

headers = [f"sat{i}" for i in range(0, 66)]
data = pd.read_csv("Scheduling-Aware-Routing/walkerStar_66_100_min_200_samples_718.csv", names=headers)

def get_position_data(satIndex: int):
    return data.iloc[:,satIndex]
