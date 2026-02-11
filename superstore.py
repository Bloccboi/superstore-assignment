import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Superstore Analysis", layout="wide")
st.title("📊 Superstore Dataset Analysis")
with st.expander("Click to see your Dataset"):
    df = pd.read_csv("sample_-_superstore.csv", encoding="latin1")
    st.write(df)


# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("sample_-_superstore.csv", encoding="latin1")
    # latin1 prevents character error
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    # coerce-invalid dates becomes NaT
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
    return df

df = load_data()


# #KPI

count_order, count_product_id, count_customer, total_sales,tot_qua, net_rev,total_profit = st.columns(7)

with count_order:
    st.metric("Total Orders", df["Order ID"].nunique())
with count_product_id:
    st.metric("Total Products", df["Product ID"].nunique())  
with count_customer:
    st.metric("Total Customers", df["Customer ID"].nunique())
with total_sales:
    st.metric("Total Sales", f"${df['Sales'].sum():,.2f}")
with tot_qua:   
    st.metric("Total Quantity", f"{df['Quantity'].sum():,.0f}")   
with net_rev:   
    df["Net Revenue"] = (df["Sales"] * df["Quantity"]) - (df["Discount"]* df["Sales"] * df["Quantity"])
    st.metric("Net Revenue", f"{df['Net Revenue'].sum():,.2f}")
with total_profit:
    st.metric("Total Profit", f"${df['Profit'].sum():,.2f}")

# In Streamlit metric is used to display a KPI

# Filters
st.sidebar.header("Filters")
region = st.sidebar.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Category", df["Category"].unique(), default=df["Category"].unique())

filtered_df = df[(df["Region"].isin(region)) & (df["Category"].isin(category))]
# Filters the dataset based on selected region AND category

st.subheader("Sales by Category")
sales_cat = filtered_df.groupby("Category")["Sales"].sum().reset_index()
fig1 = px.bar(sales_cat, x="Category", y="Sales", text_auto=True, color="Category")
st.plotly_chart(fig1, use_container_width=True)


st.subheader("Profit by Category")
profit_cat = filtered_df.groupby("Category")["Profit"].sum().reset_index()
fig2 = px.bar(profit_cat, x="Category", y="Profit", text_auto=True, color="Category")
st.plotly_chart(fig2, use_container_width=True)


st.subheader("Monthly Sales Trend")
monthly = filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index() 
monthly["Order Date"] = monthly["Order Date"].astype(str)
fig3 = px.line(monthly, x="Order Date", y="Sales", markers=True)
st.plotly_chart(fig3, use_container_width=True)

#Top 10 Products
st.subheader("Top 10 Products by Sales")
top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .nlargest(10)
    .sort_values()
    .reset_index()
)
fig4 = px.bar(top_products, x="Sales", y="Product Name", orientation="h", text_auto=True)
st.plotly_chart(fig4, use_container_width=True)

#Table
st.subheader("Region Performance Table")
region_table = filtered_df.groupby("Region")[["Sales", "Profit"]].sum().sort_values(by="Sales", ascending=False)
st.dataframe(region_table, use_container_width=True)


