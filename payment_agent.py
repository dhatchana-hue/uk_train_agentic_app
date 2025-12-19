def payment_confirmation_agent(amount_gbp: float, method: str = "Card"):
    return {
        "amount_gbp": float(amount_gbp),
        "method": method,
        "payment_status": "SUCCESS",
        "transaction_id": "TX123456"
    }

