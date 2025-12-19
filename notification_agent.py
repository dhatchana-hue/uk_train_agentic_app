def notification_agent(booking, payment):
    if payment["payment_status"] != "SUCCESS":
        return (
            "❌ Payment Failed!\n"
            f"Amount: £{payment['amount_gbp']:.2f}\n"
            "Please try again."
        )

    return (
        "✅ Booking Confirmed!\n"
        f"Train: {booking['train_name']} (ID: {booking['train_id']})\n"
        f"Route: {booking['source']} → {booking['destination']}\n"
        f"Class: {booking['class']} | Coach: {booking['coach']}\n"
        f"Seat: {booking['seat_label']} ({booking['seat_type']})\n"
        "Payment Status: SUCCESS\n"
        "Have a safe journey 🚆"
    )



