import pandas as pd


# get technology table (csv)
def get_technology():
    return pd.read_csv(f"./modules/vehicle_stock/tech_choice/data/technology.csv")


def do_something():
    p = get_technology()
    return p.head()
