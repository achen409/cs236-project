import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# connects to frontend
engine = create_engine(
    "postgresql+psycopg2://postgres:password@localhost:5432/bookings"
)

# ======Initialization======
# title
st.title("Bookings Database Viewer")

# connect tables to frontend
table_map = {
    "Customer Reservations": "customer_reservations",
    "Hotel Booking": "hotel_booking",
    "All Bookings": "all_bookings",
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
def make_slider_float(col_name, display_name, filtered, df):
    if col_name not in df.columns:
        return df

    min_val, max_val = float(df[col_name].min()), float(df[col_name].max())
    val_range = st.sidebar.slider(display_name, min_val, max_val, (min_val, max_val))
    filtered = filtered[
        (filtered[col_name] >= val_range[0]) & (filtered[col_name] <= val_range[1])
    ]
    return filtered


# for int
def make_slider(col_name, display_name, filtered, df):
    if col_name not in df.columns:
        return df

    min_val, max_val = int(df[col_name].min()), int(df[col_name].max())
    val_range = st.sidebar.slider(display_name, min_val, max_val, (min_val, max_val))
    filtered = filtered[
        (filtered[col_name] >= val_range[0]) & (filtered[col_name] <= val_range[1])
    ]
    return filtered


# categorical filters
def make_categorical_selector(col_name, display_name, filtered, df):
    if col_name not in df.columns:
        return df

    statuses = sorted(df[col_name].unique().tolist())
    selected_statuses = st.sidebar.multiselect(display_name, statuses, default=statuses)
    filtered = filtered[filtered[col_name].isin(selected_statuses)]

    return filtered


# ======Individual Filters======
df_filtered = df
# stay in weekend nights
df_filtered = make_slider(
    "stays_in_weekend_nights", "Stay in Weekend Nights", df_filtered, df
)
# stay in week nights
df_filtered = make_slider(
    "stays_in_week_nights", "Stay in Week Nights", df_filtered, df
)
# lead time
df_filtered = make_slider("lead_time", "Lead Time", df_filtered, df)
# avg price per room
df_filtered = make_slider_float(
    "avg_price_per_room", "Average Price per Room", df_filtered, df
)
# year of arrival
df_filtered = make_slider("arrival_year", "Year", df_filtered, df)
# month of arrival
df_filtered = make_slider("arrival_month", "Month", df_filtered, df)
# day of arrival
df_filtered = make_slider("arrival_day", "Day", df_filtered, df)

# booking status filter
df_filtered = make_categorical_selector(
    "booking_status", "Booking Status", df_filtered, df
)

# market segment type filter
df_filtered = make_categorical_selector(
    "market_segment_type", "Market Segment Type", df_filtered, df
)

# print filtered data
st.write(f"### Filtered Results ({len(df_filtered)} rows)")
st.dataframe(df_filtered)
