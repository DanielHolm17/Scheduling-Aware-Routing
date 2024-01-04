import pandas as pd

headers = [f"sat{i}" for i in range(0,528)]
data_718 = []

data_718.append(pd.read_csv("Scheduling-Aware-Routing/walkerStar_66_100_min_200_samples_718.csv", names=headers))
data_718.append(pd.read_csv("Scheduling-Aware-Routing/walkerStar_132_100_min_200_samples_718.csv", names=headers))
data_718.append(pd.read_csv("Scheduling-Aware-Routing/walkerStar_264_100_min_200_samples_718.csv", names=headers))
data_718.append(pd.read_csv("Scheduling-Aware-Routing/walkerStar_396_100_min_200_samples_718.csv", names=headers))
data_718.append(pd.read_csv("Scheduling-Aware-Routing/walkerStar_528_100_min_200_samples_718.csv", names=headers))

def get_element(value):
    element_mapping = {
        66: 0,
        132: 1,
        264: 2,
        396: 3,
        528: 4
    }
    return element_mapping.get(value, -1)

def get_position_data(satIndex: int, num_nodes: int):
    return data_718[get_element(num_nodes)].iloc[:,satIndex]
