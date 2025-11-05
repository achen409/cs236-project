import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/bookings")

# ======Initialization======
# title
st.title("Bookings Database Viewer")

# list tables
table_map = {
    "Customer Reservations": "customer_reservations",
    "Hotel Booking": "hotel_booking",
    "All Bookings": "all_bookings"
}
table_label = st.sidebar.selectbox("Select dataset", list(table_map.keys()))
table_name = table_map[table_label]

# load data function
@st.cache_data
def load_data(table):
    query = text(f"SELECT * FROM {table};")
    return pd.read_sql(query, engine)



# ======Load Function======
# call load function
# create ui as well
df = load_data(table_name)
st.write(f"### Showing `{table_name}` ({len(df)} rows loaded)")
st.dataframe(df.head(5))



# ======Filters======
# filter ui on left sidebar
st.sidebar.header("Filter options")

# numeric filters
if "avg_price_per_room" in df.columns:
    min_price, max_price = float(df["avg_price_per_room"].min()), float(df["avg_price_per_room"].max())
    price_range = st.sidebar.slider(
        "Average Price Per Room", min_price, max_price, (min_price, max_price)
    )
    df = df[(df["avg_price_per_room"] >= price_range[0]) & (df["avg_price_per_room"] <= price_range[1])]

# booking status filter
if "booking_status" in df.columns:
    statuses = sorted(df["booking_status"].unique().tolist())
    selected_statuses = st.sidebar.multiselect("Booking Status", statuses, default=statuses)
    df = df[df["booking_status"].isin(selected_statuses)]

# market segment type filter
if "market_segment_type" in df.columns:
    segments = sorted(df["market_segment_type"].unique().tolist())
    selected_segments = st.sidebar.multiselect("Market Segment Type", segments, default=segments)
    df = df[df["market_segment_type"].isin(selected_segments)]

# print filtered data
st.write(f"### Filtered Results ({len(df)} rows)")
st.dataframe(df)