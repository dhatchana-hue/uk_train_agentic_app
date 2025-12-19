from typing import List, Dict
import random

def seat_availability_agent(seat_map: List[Dict], booked_count: int, seed: int = 7) -> List[Dict]:
    random.seed(seed)
    booked_count = max(0, min(booked_count, len(seat_map)))
    booked_ids = set(random.sample([s["seat_id"] for s in seat_map], booked_count))

    for s in seat_map:
        s["status"] = "Booked" if s["seat_id"] in booked_ids else "Available"
    return seat_map
