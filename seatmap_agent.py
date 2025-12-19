from typing import List, Dict

def seat_map_generation_agent(total_seats: int) -> List[Dict]:
    """
    Generates a simple grid-friendly seat map.
    Seat labels like 1A, 1B, 1C, 1D ... (4 seats per row)
    """
    seats = []
    letters = ["A", "B", "C", "D"]  # 4 seats per row
    rows = total_seats // 4

    seat_no = 1
    for r in range(1, rows + 1):
        for c in letters:
            label = f"{r}{c}"
            seat_type = "Window" if c in ["A", "D"] else "Aisle"
            seats.append({
                "seat_id": seat_no,
                "seat_label": label,
                "seat_type": seat_type,
                "status": "Available"
            })
            seat_no += 1

    return seats
