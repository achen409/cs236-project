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



# ======Filter Functions======
# filter ui on left sidebar
st.sidebar.header("Filter options")

# numeric slider filters (for float)
def make_slider_float(col_name, display_name, df):
    if col_name not in df.columns:
        return df
    
    min_val, max_val = float(df[col_name].min()), float(df[col_name].max())
    val_range = st.sidebar.slider(
        display_name, min_val, max_val, (min_val, max_val)
    )
    df = df[(df[col_name] >= val_range[0]) & (df[col_name] <= val_range[1])]
    return df

# for int
def make_slider(col_name, display_name, df):
    if col_name not in df.columns:
        return df
    
    min_val, max_val = int(df[col_name].min()), int(df[col_name].max())
    val_range = st.sidebar.slider(
        display_name, min_val, max_val, (min_val, max_val)
    )
    df = df[(df[col_name] >= val_range[0]) & (df[col_name] <= val_range[1])]
    return df


# categorical filters
def make_categorical_selector(col_name, display_name, df):
    if col_name not in df.columns:
        return df
    
    statuses = sorted(df[col_name].unique().tolist())
    selected_statuses = st.sidebar.multiselect(display_name, statuses, default=statuses)
    df = df[df[col_name].isin(selected_statuses)]

    return df


# ======Individual Filters======
# stay in weekend nights
df = make_slider("stays_in_weekend_nights", "Stay in Weekend Nights", df)
# stay in week nights
df = make_slider("stays_in_week_nights", "Stay in Week Nights", df)
# lead time
df = make_slider("lead_time", "Lead Time", df)
# avg price per room
df = make_slider_float("avg_price_per_room", "Average Price per Room", df)

# TODO: 3 Date vars (year, month, day)

# booking status filter
df = make_categorical_selector("booking_status", "Booking Status", df)

# market segment type filter
df = make_categorical_selector("market_segment_type", "Market Segment Type", df)

# print filtered data
st.write(f"### Filtered Results ({len(df)} rows)")
st.dataframe(df)