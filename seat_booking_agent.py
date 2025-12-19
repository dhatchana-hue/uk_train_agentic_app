from typing import List, Dict, Tuple

def seat_booking_agent(seat_map: List[Dict], chosen_seat_label: str) -> Tuple[bool, str]:
    for s in seat_map:
        if s["seat_label"] == chosen_seat_label:
            if s["status"] == "Booked":
                return False, "Seat already booked"
            s["status"] = "Booked"
            return True, "Seat booked successfully"
    return False, "Seat not found"
