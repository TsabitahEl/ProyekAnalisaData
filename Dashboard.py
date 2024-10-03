import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Function Definitions
def highest_customer(customers_df):
    city_counts = customers_df['customer_city'].value_counts().reset_index()
    city_counts.columns = ['customer_city', 'customer_count']
    return city_counts

def payment_type(order_payments_df):
    payment_type_counts = order_payments_df['payment_type'].value_counts().reset_index()
    payment_type_counts.columns = ['payments_type', 'payment_type_count']
    return payment_type_counts

def order_compare(orders_df):
    delivered_orders_df = orders_df[orders_df['order_status'] == 'delivered']
    delivered_orders_df['order_purchase_timestamp'] = pd.to_datetime(delivered_orders_df['order_purchase_timestamp'])
    delivered_orders_df = delivered_orders_df.set_index('order_purchase_timestamp')
    
    monthly_delivered_df = delivered_orders_df.resample('M').agg({"order_id": "nunique"}).rename(columns={"order_id": "delivered_count"})
    monthly_delivered_df.index = monthly_delivered_df.index.strftime('%Y-%m')
    monthly_delivered_df = monthly_delivered_df.reset_index().rename(columns={"order_purchase_timestamp": "order_date"})
    
    # Extracting year and month for plotting
    monthly_delivered_df['year'] = pd.to_datetime(monthly_delivered_df['order_date']).dt.year
    monthly_delivered_df['month'] = pd.to_datetime(monthly_delivered_df['order_date']).dt.month
    return monthly_delivered_df

# Load Data
cust_correct = pd.read_csv('customers_corrected.csv')
ord_correct = pd.read_csv('orders_corrected.csv')
ord_payment = pd.read_csv('order_payments_corrected.csv')

# Process Data
high_cust = highest_customer(cust_correct)  # Changed from city_counts to high_cust
pay_type = payment_type(ord_payment)
ord_comp = order_compare(ord_correct)

# Streamlit Visualization
st.header('E-Commerce Public Analysis')

# Cities by Number of Customers
st.subheader("Cities by Number of Customers")
fig, ax = plt.subplots()
colors = ["#3A6D8C", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="customer_count", y="customer_city", data=high_cust.head(5), palette=colors, ax=ax)  # Using high_cust
ax.set_ylabel("Name of City")
ax.set_xlabel("Number of Customers")
ax.set_title("Top 5 Cities with Most Customers", loc="center", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)

# Payment Types
st.subheader("Top Payment Types Used")
fig, ax = plt.subplots(figsize=(12, 6))
colors = ["#3A6D8C", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="payment_type_count", y="payments_type", data=pay_type.head(5), palette=colors, ax=ax)  # Using pay_type
ax.set_ylabel("Payment Type")
ax.set_xlabel("Number of Payments")
ax.set_title("Top 5 Payment Types Most Used", loc="center", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)

# Orders comparison (2016-2018)
st.subheader("Total Orders by Month (2016-2018)")
fig, ax = plt.subplots(figsize=(12, 6))

# List of contrasting colors for each year
colors = plt.cm.get_cmap('tab20', len(ord_comp['year'].unique()))

# Loop for plotting each year with different colors
for i, year in enumerate(ord_comp['year'].unique()):
    year_data = ord_comp[ord_comp['year'] == year]
    ax.plot(year_data['month'], year_data['delivered_count'], label=str(year), color=colors(i), marker='o', linewidth=2)

# Title and labels
ax.set_xlabel("Month", fontsize=15)
ax.set_ylabel("Number of Delivered Orders", fontsize=15)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=10)
ax.legend(title="Year", fontsize=12)
plt.tight_layout()
st.pyplot(fig)
