import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Motor Vehicle Theft Interactive Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    thefts = pd.read_csv("stolen_vehicles.csv")
    locations = pd.read_csv("locations.csv")
    makes = pd.read_csv("make_details.csv")

    # Clean column names
    thefts.columns = thefts.columns.str.lower().str.strip()
    locations.columns = locations.columns.str.lower().str.strip()
    makes.columns = makes.columns.str.lower().str.strip()

    # Merge datasets
    df = thefts.merge(locations, on="location_id", how="left")
    df = df.merge(makes, on="make_id", how="left")

    return df

df = load_data()

# DATA CLEANING

df = df.drop_duplicates()

df["date_stolen"] = pd.to_datetime(df["date_stolen"], errors="coerce")
df = df.dropna(subset=["date_stolen"])

df["year"] = df["date_stolen"].dt.year
df["month"] = df["date_stolen"].dt.month
df["month_name"] = df["date_stolen"].dt.month_name()

# Fill missing categorical values
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].fillna("Unknown")


st.title("🚗 Motor Vehicle Theft Interactive Dashboard")
st.markdown("An analytical overview of stolen vehicle patterns by region, make, type and season.")


# SIDEBAR FILTERS

st.sidebar.header("Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

vehicle_filter = st.sidebar.multiselect(
    "Select Vehicle Type",
    sorted(df["vehicle_type"].unique()),
    default=sorted(df["vehicle_type"].unique())
)

filtered_df = df[
    (df["year"].isin(year_filter)) &
    (df["region"].isin(region_filter)) &
    (df["vehicle_type"].isin(vehicle_filter))
]

# DASHBOARD TABS


tab1, tab2, tab3 = st.tabs([
    "📊 Overview",
    "🌍 Regional Analysis",
    "📈 Trends & Patterns"
])


# 📊 TAB 1 — EXECUTIVE OVERVIEW


with tab1:

    st.subheader("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Thefts", len(filtered_df))
    col2.metric("Regions Covered", filtered_df["region"].nunique())
    col3.metric("Vehicle Types", filtered_df["vehicle_type"].nunique())
    col4.metric("Vehicle Makes", filtered_df["make_name"].nunique())

   

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("Most Stolen Vehicle",
                filtered_df["vehicle_type"].mode()[0])

    col6.metric("Most Affected Region",
                filtered_df["region"].mode()[0])

    col7.metric("Most Stolen Make",
                filtered_df["make_name"].mode()[0])

    col8.metric("Peak Month",
                filtered_df["month_name"].mode()[0])

    st.markdown("---")

    with st.expander("Click to View Dataset"):
        st.dataframe(filtered_df, use_container_width=True)


# 🌍 TAB 2 — REGIONAL ANALYSIS


with tab2:

    st.subheader("Vehicle Thefts by Region")

    region_counts = filtered_df["region"].value_counts().reset_index()
    region_counts.columns = ["Region", "Count"]

    fig_region = px.bar(
        region_counts,
        x="Region",
        y="Count",
        title="Vehicle Thefts by Region"
    )

    st.plotly_chart(fig_region, use_container_width=True)

    st.markdown("---")

    st.subheader("Top 10 Stolen Vehicle Types")

    vehicle_counts = filtered_df["vehicle_type"].value_counts().head(10)

    fig_vehicle = px.bar(
        x=vehicle_counts.values,
        y=vehicle_counts.index,
        orientation="h",
        labels={"x": "Count", "y": "Vehicle Type"}
    )

    st.plotly_chart(fig_vehicle, use_container_width=True)

    st.markdown("---")

    st.subheader("Top 5 Most Stolen Vehicle Makes")

    top_makes = (
        filtered_df["make_name"]
        .value_counts()
        .head(5)
        .reset_index()
    )

    top_makes.columns = ["Make", "Count"]

    fig_make = px.bar(
        top_makes,
        x="Count",
        y="Make",
        orientation="h",
        title="Top 5 Most Targeted Vehicle Brands",
        labels={"Count": "Total Thefts"}
    )

    fig_make.update_layout(yaxis=dict(autorange="reversed"))

    st.plotly_chart(fig_make, use_container_width=True)

# 📈 TAB 3 — TRENDS & PATTERNS


with tab3:

    st.subheader("Daily Vehicle Theft Trend")

    trend = filtered_df.groupby("date_stolen").size().reset_index(name="count")

    fig_trend = px.line(
        trend,
        x="date_stolen",
        y="count",
        title="Daily Theft Trend"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    st.subheader("Monthly Seasonality Trend")

    monthly_counts = (
        filtered_df
        .groupby("month_name")
        .size()
        .reset_index(name="count")
    )

    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    monthly_counts["month_name"] = pd.Categorical(
        monthly_counts["month_name"],
        categories=month_order,
        ordered=True
    )

    monthly_counts = monthly_counts.sort_values("month_name")

    fig_month = px.line(
        monthly_counts,
        x="month_name",
        y="count",
        markers=True,
        title="Vehicle Theft Seasonal Pattern",
        labels={"month_name": "Month", "count": "Total Thefts"}
    )

    fig_month.update_traces(line=dict(width=3))

    st.plotly_chart(fig_month, use_container_width=True)

    st.markdown("---")

    st.subheader("Theft by Day of Week")

    day_counts = filtered_df["date_stolen"].dt.day_name().value_counts()

    fig_day = px.bar(
        x=day_counts.index,
        y=day_counts.values,
        labels={"x": "Day", "y": "Count"}
    )

    st.plotly_chart(fig_day, use_container_width=True)

    st.markdown("---")

    st.subheader("Key Insights")

    top_region = filtered_df["region"].mode()[0]
    top_vehicle = filtered_df["vehicle_type"].mode()[0]
    top_make = filtered_df["make_name"].mode()[0]
    peak_month = filtered_df["month_name"].mode()[0]

    st.write(f"""
    • **{top_region}** is the most affected region for vehicle theft.  
    • **{top_vehicle}** is the most frequently stolen vehicle type.  
    • **{top_make}** is the most targeted vehicle brand.  
    • Theft activity peaks in **{peak_month}**, suggesting seasonal influence.  
    • Theft patterns show consistent activity across weekdays, indicating structured criminal behavior.
    """)