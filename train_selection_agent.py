import pandas as pd

def train_selection_agent(df: pd.DataFrame, source: str, destination: str, travel_class: str) -> pd.DataFrame:
    res = df[
        (df["source"] == source) &
        (df["destination"] == destination) &
        (df["class"] == travel_class)
    ].copy()

    # sort: most seats first
    res = res.sort_values(["seat_available", "train_name"], ascending=[False, True])
    return res
