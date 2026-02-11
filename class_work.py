import streamlit as st
import pandas as pd
import numpy as np 



st.set_page_config(page_title="Data Viz App", layout="wide")
st.title("Data vizualization App")

## Hide the dataset 

with st.expander("Click to see your Dataset"):
    df = pd.read_csv("sample_-_superstore.csv", encoding="latin1")
    st.write(df)

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



table_col, chart_col = st.columns(2)
#  ------------------------------------------first column---------------------------
with table_col:
    sale_tab, profit_tab = st.tabs(["Sales by Category", "Profit by Category"])

    # ----------------------------sales by category---------------------------
    with sale_tab:
        st.header("Sales by Category")
        sales_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False) #.reset_index()
        st.dataframe(sales_category)

    # ----------------------------profit by category---------------------------
    with profit_tab:
        st.header("Profit by Category")
        profit_category = df.groupby("Category")["Profit"].sum().sort_values(ascending=False) #.reset_index()
        st.dataframe(profit_category)


timeseries_col, piechart_col = st.columns(2)
#  ------------------------------------------second column---------------------------
with timeseries_col:
    st.header("Sales Over Time")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    sales_time = df.groupby("Order Date")["Sales"].sum()
    st.line_chart(sales_time)
