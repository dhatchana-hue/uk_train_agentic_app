import streamlit as st
import pandas as pd

from dataset_agent import generate_uk_train_dataset, UK_CITIES, CLASSES
from train_selection_agent import train_selection_agent
from coach_selection_agent import coach_selection_agent
from seatmap_agent import seat_map_generation_agent
from seat_availability_agent import seat_availability_agent
from seat_booking_agent import seat_booking_agent
from payment_agent import payment_confirmation_agent
from notification_agent import notification_agent

st.set_page_config(page_title="UK Agentic AI Train Booking", layout="centered")
st.title("🚆 UK Agentic AI Train Ticket Booking")
st.caption("Workflow: Train → Coach → Seat Map → Availability → Seat Select → Booking → Payment → Notification")

# Dataset (cached)
@st.cache_data
def load_data():
    return generate_uk_train_dataset(n_trains=120, seed=42)

df = load_data()

# Session state
if "selected_train_id" not in st.session_state:
    st.session_state.selected_train_id = None
if "selected_coach" not in st.session_state:
    st.session_state.selected_coach = None
if "seat_map" not in st.session_state:
    st.session_state.seat_map = None
if "chosen_seat_label" not in st.session_state:
    st.session_state.chosen_seat_label = None

# ---------------------------
# USER INPUT
# ---------------------------
st.subheader("🧾 User Input")
req = st.text_input("Request", "London to Manchester standard ticket")
source = st.selectbox("Source (UK)", UK_CITIES, index=0)
destination = st.selectbox("Destination (UK)", UK_CITIES, index=1)
travel_class = st.selectbox("Class", CLASSES, index=0)

# ---------------------------
# Train Selection Agent
# ---------------------------
if st.button("🔎 Search Trains"):
    st.session_state.selected_train_id = None
    st.session_state.selected_coach = None
    st.session_state.seat_map = None
    st.session_state.chosen_seat_label = None

    st.markdown("## ⚙️ Agent Evidence")

    st.success("1) Train Selection Agent ✔")
    trains = train_selection_agent(df, source, destination, travel_class)

    if trains.empty:
        st.error("No trains found for this route/class. Try different cities.")
        st.stop()

    # show top trains (unique train ids)
    top_trains = trains[["train_id", "train_name"]].drop_duplicates().head(8)
    st.dataframe(top_trains, use_container_width=True)

    # train choose
    options = top_trains.apply(lambda r: f"{r.train_name} | ID:{r.train_id}", axis=1).tolist()
    chosen = st.radio("Select a train", options)
    chosen_id = int(chosen.split("ID:")[1].strip())
    st.session_state.selected_train_id = chosen_id

# ---------------------------
# Coach Selection Agent
# ---------------------------
if st.session_state.selected_train_id is not None:
    st.success("2) Coach Selection Agent ✔")
    trains_for_route = train_selection_agent(df, source, destination, travel_class)
    coach_df = coach_selection_agent(trains_for_route, st.session_state.selected_train_id)

    st.dataframe(coach_df[["coach", "total_seats", "booked_seats", "seat_available"]], use_container_width=True)

    coach_options = coach_df.apply(
        lambda r: f"{r.coach} | Available:{int(r.seat_available)} / {int(r.total_seats)}",
        axis=1
    ).tolist()

    chosen_coach = st.selectbox("Select Coach", coach_options)
    st.session_state.selected_coach = chosen_coach.split("|")[0].strip()

    selected_row = coach_df[coach_df["coach"] == st.session_state.selected_coach].iloc[0]

    # ---------------------------
    # Seat Map Generation + Availability
    # ---------------------------
    st.success("3) Seat Map Generation Agent ✔")
    seat_map = seat_map_generation_agent(int(selected_row["total_seats"]))

    st.success("4) Seat Availability Agent ✔")
    seat_map = seat_availability_agent(
        seat_map=seat_map,
        booked_count=int(selected_row["booked_seats"]),
        seed=int(selected_row["train_id"]) % 100
    )
    st.session_state.seat_map = seat_map

    # ---------------------------
    # User Seat Selection (Grid UI)
    # ---------------------------
    st.markdown("## 🪑 User Seat Selection (Grid UI)")
    st.caption("🟢 Available | 🔴 Booked — click an Available seat")

    # Build grid 4 columns
    cols = st.columns(4)
    chosen_label = None

    for i, seat in enumerate(st.session_state.seat_map):
        col = cols[i % 4]
        with col:
            if seat["status"] == "Booked":
                st.button(f"🔴 {seat['seat_label']}", key=f"b_{seat['seat_label']}", disabled=True)
            else:
                if st.button(f"🟢 {seat['seat_label']}", key=f"a_{seat['seat_label']}"):
                    chosen_label = seat["seat_label"]
                    st.session_state.chosen_seat_label = chosen_label

    if st.session_state.chosen_seat_label:
        # show selected seat details
        seat_obj = next(s for s in st.session_state.seat_map if s["seat_label"] == st.session_state.chosen_seat_label)
        st.info(f"Selected Seat: **{seat_obj['seat_label']}** ({seat_obj['seat_type']})")

        # ---------------------------
        # Seat Booking Agent
        # ---------------------------
        if st.button("🎟️ Confirm Seat Booking"):
            st.success("5) Seat Booking Agent ✔")
            ok, msg = seat_booking_agent(st.session_state.seat_map, st.session_state.chosen_seat_label)

            if not ok:
                st.error(f"Booking failed: {msg}")
                st.stop()

            # booking object
            booking = {
                "train_id": int(selected_row["train_id"]),
                "train_name": str(selected_row["train_name"]),
                "source": str(selected_row["source"]),
                "destination": str(selected_row["destination"]),
                "class": str(selected_row["class"]),
                "coach": str(selected_row["coach"]),
                "seat_label": seat_obj["seat_label"],
                "seat_type": seat_obj["seat_type"],
            }

            # ---------------------------
            # Payment Confirmation Agent
            # ---------------------------
            st.success("6) Payment Confirmation Agent ✔")
            amount = 35.00 if travel_class == "Standard" else 85.00
          payment = payment_confirmation_agent(amount_gbp=amount, method="Card")

            # ---------------------------
            # Notification Agent
            # ---------------------------
            st.success("7) Notification Agent ✔")
            final_msg = notification_agent(booking, payment)

            st.markdown("## 📩 Final Output")
            if payment["payment_status"] == "SUCCESS":
                st.success(final_msg)
            else:
                st.error(final_msg)
