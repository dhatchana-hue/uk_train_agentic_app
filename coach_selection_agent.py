import pandas as pd

def coach_selection_agent(trains_df: pd.DataFrame, train_id: int) -> pd.DataFrame:
    coaches = trains_df[trains_df["train_id"] == train_id].copy()
    coaches = coaches.sort_values("seat_available", ascending=False)
    return coaches
