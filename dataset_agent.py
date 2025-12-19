import pandas as pd
import numpy as np

UK_CITIES = ["London", "Manchester", "Birmingham", "Leeds", "Liverpool", "Edinburgh", "Glasgow"]
CLASSES = ["Standard", "First"]

def generate_uk_train_dataset(n_trains=120, seed=42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    rows = []
    for i in range(n_trains):
        src = rng.choice(UK_CITIES)
        dst = rng.choice(UK_CITIES)
        while dst == src:
            dst = rng.choice(UK_CITIES)

        travel_class = rng.choice(CLASSES, p=[0.8, 0.2])

        train_id = int(70000 + i)
        train_name = f"UK_Express_{int(rng.integers(1, 300))}"

        # Each train has multiple coaches
        coaches = ["C1", "C2", "C3"] if travel_class == "Standard" else ["F1", "F2"]
        total_seats = 48 if travel_class == "First" else 72

        for coach in coaches:
            booked = int(rng.integers(10, total_seats + 1))
            rows.append({
                "train_id": train_id,
                "train_name": train_name,
                "source": str(src),
                "destination": str(dst),
                "class": str(travel_class),
                "coach": str(coach),
                "total_seats": total_seats,
                "booked_seats": booked,
                "seat_available": total_seats - booked
            })

    return pd.DataFrame(rows)
