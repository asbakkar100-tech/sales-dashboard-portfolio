import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Analytics Dashboard")
st.write("Interactive dashboard for analyzing sales performance by region, product, and time.")

df = pd.read_csv("sales_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Sidebar filters
st.sidebar.header("🔎 Filters")

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)

selected_products = st.sidebar.multiselect(
    "Select Product",
    options=df["product"].unique(),
    default=df["product"].unique()
)

filtered_df = df[
    (df["region"].isin(selected_regions)) &
    (df["product"].isin(selected_products))
]

# KPIs
total_revenue = filtered_df["revenue"].sum()
total_units = filtered_df["units_sold"].sum()
total_orders = len(filtered_df)
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Units Sold", f"{total_units:,}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Avg Order Value", f"${avg_order_value:,.0f}")

st.divider()

# Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Revenue Over Time")
    revenue_time = filtered_df.groupby("date")["revenue"].sum()

    fig, ax = plt.subplots()
    ax.plot(revenue_time.index, revenue_time.values)
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    ax.set_title("Daily Revenue Trend")
    st.pyplot(fig)

with col_right:
    st.subheader("🌍 Revenue by Region")
    region_revenue = filtered_df.groupby("region")["revenue"].sum().sort_values(ascending=False)

    fig2, ax2 = plt.subplots()
    region_revenue.plot(kind="bar", ax=ax2)
    ax2.set_xlabel("Region")
    ax2.set_ylabel("Revenue")
    ax2.set_title("Revenue by Region")
    st.pyplot(fig2)

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("💻 Revenue by Product")
    product_revenue = filtered_df.groupby("product")["revenue"].sum().sort_values(ascending=False)

    fig3, ax3 = plt.subplots()
    product_revenue.plot(kind="bar", ax=ax3)
    ax3.set_xlabel("Product")
    ax3.set_ylabel("Revenue")
    ax3.set_title("Revenue by Product")
    st.pyplot(fig3)

with col_right2:
    st.subheader("📦 Units Sold by Product")
    product_units = filtered_df.groupby("product")["units_sold"].sum().sort_values(ascending=False)

    fig4, ax4 = plt.subplots()
    product_units.plot(kind="bar", ax=ax4)
    ax4.set_xlabel("Product")
    ax4.set_ylabel("Units Sold")
    ax4.set_title("Units Sold by Product")
    st.pyplot(fig4)

st.divider()

# Business insights
st.subheader("🧠 Business Insights")

if not filtered_df.empty:
    best_region = filtered_df.groupby("region")["revenue"].sum().idxmax()
    best_product = filtered_df.groupby("product")["revenue"].sum().idxmax()
    best_day = filtered_df.groupby("date")["revenue"].sum().idxmax().date()

    st.success(f"Best performing region: **{best_region}**")
    st.success(f"Top revenue product: **{best_product}**")
    st.info(f"Highest revenue day: **{best_day}**")

    st.write(
        "This dashboard helps business owners quickly identify revenue trends, "
        "top-performing regions, and best-selling products."
    )
else:
    st.warning("No data available for the selected filters.")

st.subheader("📋 Filtered Data")
st.dataframe(filtered_df)