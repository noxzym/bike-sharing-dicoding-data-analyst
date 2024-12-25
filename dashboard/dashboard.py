import streamlit as st
import pandas as pd
import plotly.express as px

# Helper Function
def initialize_data():
    season = [
        "Spring",
        "Summer",
        "Fall",
        "Winter",
    ]

    year = [
        2011,
        2012,
    ]

    month = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    weather = [
        "Clear",
        "Mist",
        "Light Rain/Snow",
        "Heavy Rain/Snow",
    ]

    for df in [day_df, hour_df]:
        df["date"] = pd.to_datetime(df["date"])
        df["season"] = pd.Categorical(df["season"], categories=season, ordered=True)
        df["year"] = pd.Categorical(df["year"], categories=year, ordered=True)
        df["month"] = pd.Categorical(df["month"], categories=month, ordered=True)
        if "weather" in df:
            df["weather"] = pd.Categorical(df["weather"], categories=weather, ordered=True)
        if "hour" in df:
            df["hour"] = pd.Categorical(df["hour"], categories=[(i) for i in range(24)], ordered=True)

def create_total_rentals():
    total_rentals = day_filter_df["total"].sum()

    st.metric(f"Total Rentals:", total_rentals, border=True, help="Total number of bike rentals in the dataset")

def create_registered_users():
    registered_users = day_filter_df["registered"].sum()

    st.metric(f"Total Registered Users:", registered_users, border=True, help="Total number of registered users in the dataset")

def create_casual_users():
    casual_users = day_filter_df["casual"].sum()

    st.metric(f"Total Casual Users:", casual_users, border=True, help="Total number of casual users in the dataset")

def create_line_chart_perform_year():
    perform_year_df = day_filter_df.groupby(["year", "month"], observed=False).agg({"total": "sum"})
    perform_year_df = perform_year_df[perform_year_df["total"] != 0]
    perform_year_df = perform_year_df.reset_index()

    if display_raw:
        st.write(perform_year_df)

    fig = px.line(perform_year_df, x="month", y="total", color="year", markers=True, labels={"value": "Total Rentals", "month": "Month"})

    st.plotly_chart(fig)


def create_bar_chart_perform_year():
    total_perform_year_df = day_filter_df.groupby("year", observed=False).agg({"total": "sum"})
    total_perform_year_df = total_perform_year_df[total_perform_year_df["total"] != 0]
    total_perform_year_df = total_perform_year_df.reset_index()

    if display_raw:
        st.write(total_perform_year_df)
        
    fig = px.bar(total_perform_year_df, x="year", y="total", color="year")
    
    st.plotly_chart(fig)

def create_bar_chart_perform_season():
    perform_season_df = day_filter_df.groupby(["season"], observed=False).agg({ "casual": "sum", "registered": "sum" })
    perform_season_df = perform_season_df[perform_season_df["casual"] != 0]
    perform_season_df = perform_season_df.reset_index()

    if display_raw:
        st.write(perform_season_df)
    
    fig = px.bar(perform_season_df, x="season", y=["casual", "registered"], barmode="relative")

    st.plotly_chart(fig)

def create_bar_chart_perform_hour():
    perform_hour_df = hour_filter_df.groupby("hour", observed=False).agg({"total": "max"})
    perform_hour_df = perform_hour_df[perform_hour_df["total"] != 0]
    perform_hour_df = perform_hour_df.reset_index()
    perform_hour_df.columns = ["hour", "max"]
    perform_hour_df["type"] = ["Peak" if i == perform_hour_df["max"].max() else "Normal" for i in perform_hour_df["max"]]

    if display_raw:
        st.write(perform_hour_df)

    fig = px.bar(perform_hour_df, x="hour", y="max", labels={"max": "Total Rentals", "hour": "Hour"}, color="type")

    st.plotly_chart(fig)

# Load data
day_df = pd.read_csv("./dashboard/day_data.csv")
hour_df = pd.read_csv("./dashboard/hour_data.csv")

# Initialize Data
initialize_data()

# Create Sidebar
with st.sidebar:
    st.title("Control Panel")
    
    # Filter by Year
    year_opts = ["All Years", *day_df["year"].cat.categories]
    filter_year = st.selectbox("Select Year:", year_opts)
    day_filter_df = day_df if filter_year == "All Years" else day_df[day_df["year"] == filter_year]
    hour_filter_df = hour_df if filter_year == "All Years" else hour_df[hour_df["year"] == filter_year]

    # Filter by Month
    month_opts = ["All Months", *day_df["month"].cat.categories]
    filter_month = st.selectbox("Select Month:", month_opts)
    day_filter_df = day_filter_df if filter_month == "All Months" else day_filter_df[day_filter_df["month"] == filter_month]
    hour_filter_df = hour_filter_df if filter_month == "All Months" else hour_filter_df[hour_filter_df["month"] == filter_month]

    # Filter by Season
    season_opts = ["All Seasons", *day_df["season"].cat.categories]
    filter_season = st.selectbox("Select Season:", season_opts)
    day_filter_df = day_filter_df if filter_season == "All Seasons" else day_filter_df[day_filter_df["season"] == filter_season]
    hour_filter_df = hour_filter_df if filter_season == "All Seasons" else hour_filter_df[hour_filter_df["season"] == filter_season]

    # Filter by Day Type
    day_type_opts = ["All Days", "Working Days", "Holidays"]
    filter_day_type = st.selectbox("Select Day Type:", day_type_opts)
    day_filter_df = day_filter_df if filter_day_type == "All Days" else day_filter_df[day_filter_df["workingday"] == (1 if filter_day_type == "Working Days" else 0)]
    hour_filter_df = hour_filter_df if filter_day_type == "All Days" else hour_filter_df[hour_filter_df["workingday"] == (1 if filter_day_type == "Working Days" else 0)]

    # Display Raw Data
    display_raw = st.checkbox("Show Raw Data")

    st.divider()

    st.markdown(
        """
        # Creator\n
        Name: Orchitiadi Ismaulana Putra\n
        Dicoding: noxzym\n
        Email: me@noxzym.my.id
        """
    )

# Create Dashboard
st.title("Bike Rentals Dashboard", help="Dashboard for displaying bike rentals statistics")

col1, col2, col3 = st.columns(3)

with col1:
    create_total_rentals()

with col2:
    create_registered_users()

with col3:
    create_casual_users()

# Display Raw Data
if display_raw:
    st.subheader("Raw Data")
    st.dataframe(day_filter_df)

# Bike Rentals Statistics by Month
if filter_month == "All Months":
    st.subheader("by Month")
    create_line_chart_perform_year()

# Bike Rentals Statistics by Year
st.subheader("by Year")
create_bar_chart_perform_year()

# Bike Rentals Statistics by Season
st.subheader("by Season")
create_bar_chart_perform_season()

# Bike Rentals Statistics by Hour
st.subheader("by Hour")
create_bar_chart_perform_hour()

st.caption("Copyright @ 2024 Orchitiadi Ismaulana Putra")