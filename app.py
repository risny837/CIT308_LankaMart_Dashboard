import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="LankaMart Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 LankaMart Sales Dashboard")
st.write("Interactive Retail Sales Analysis Dashboard")

# =========================
# LOAD CSV
# =========================

df = pd.read_csv("CIT308_LankaMart_Retail_Transactions.csv")

df.columns = df.columns.str.strip().str.lower()

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

df["revenue_lkr"] = pd.to_numeric(
    df["revenue_lkr"],
    errors="coerce"
)

df["cost_lkr"] = pd.to_numeric(
    df["cost_lkr"],
    errors="coerce"
)

df["profit_lkr"] = pd.to_numeric(
    df["profit_lkr"],
    errors="coerce"
)

df["units"] = pd.to_numeric(
    df["units"],
    errors="coerce"
)

df["customer_rating"] = pd.to_numeric(
    df["customer_rating"],
    errors="coerce"
)

df["delivery_days"] = pd.to_numeric(
    df["delivery_days"],
    errors="coerce"
)

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("🔎 Filters")

province_list = sorted(
    df["province"].dropna().astype(str).unique().tolist()
)

selected_province = st.sidebar.selectbox(
    "Select Province",
    ["All"] + province_list
)

category_list = sorted(
    df["product_category"].dropna().astype(str).unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Select Product Category",
    ["All"] + category_list
)

segment_list = sorted(
    df["customer_segment"].dropna().astype(str).unique().tolist()
)

selected_segment = st.sidebar.selectbox(
    "Select Customer Segment",
    ["All"] + segment_list
)

# =========================
# DATE FILTER
# =========================

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# =========================
# APPLY FILTERS
# =========================

filtered_df = df.copy()

if selected_province != "All":
    filtered_df = filtered_df[
        filtered_df["province"].astype(str) == selected_province
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["product_category"].astype(str) == selected_category
    ]

if selected_segment != "All":
    filtered_df = filtered_df[
        filtered_df["customer_segment"].astype(str) == selected_segment
    ]

if len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

    filtered_df = filtered_df[
        (filtered_df["order_date"] >= start_date)
        & (filtered_df["order_date"] <= end_date)
    ]

# =========================
# KPI CALCULATIONS
# =========================

total_revenue = filtered_df["revenue_lkr"].sum()
total_cost = filtered_df["cost_lkr"].sum()
total_profit = filtered_df["profit_lkr"].sum()
total_orders = len(filtered_df)

# =========================
# KPI SECTION
# =========================

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Revenue",
    f"LKR {total_revenue:,.2f}"
)

col2.metric(
    "💸 Total Cost",
    f"LKR {total_cost:,.2f}"
)

col3.metric(
    "📈 Total Profit",
    f"LKR {total_profit:,.2f}"
)

col4.metric(
    "🧾 Total Orders",
    f"{total_orders:,}"
)

# =========================
# SALES DATA
# =========================

st.subheader("📋 Sales Data")

st.dataframe(
    filtered_df,
    width="stretch"
)

# =========================
# DOWNLOAD DATA
# =========================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv_data,
    file_name="LankaMart_Filtered_Data.csv",
    mime="text/csv"
)

# =========================
# REVENUE & PROFIT BY PROVINCE
# =========================

st.subheader("📍 Revenue & Profit by Province")

province_sales = (
    filtered_df
    .groupby("province")[["revenue_lkr", "profit_lkr"]]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    province_sales,
    x="province",
    y=["revenue_lkr", "profit_lkr"],
    barmode="group",
    title="Revenue & Profit by Province",
    labels={
        "value": "Amount (LKR)",
        "province": "Province",
        "variable": "Metric"
    }
)

st.plotly_chart(
    fig1,
    width="stretch"
)

# =========================
# REVENUE BY PRODUCT CATEGORY
# =========================

st.subheader("🛍️ Revenue by Product Category")

category_sales = (
    filtered_df
    .groupby("product_category")["revenue_lkr"]
    .sum()
    .reset_index()
    .sort_values(
        "revenue_lkr",
        ascending=False
    )
)

fig2 = px.bar(
    category_sales,
    x="product_category",
    y="revenue_lkr",
    title="Revenue by Product Category",
    labels={
        "revenue_lkr": "Revenue (LKR)",
        "product_category": "Product Category"
    }
)

st.plotly_chart(
    fig2,
    width="stretch"
)

# =========================
# DAILY REVENUE
# =========================

st.subheader("📅 Daily Revenue")

daily_revenue = (
    filtered_df
    .groupby("order_date")["revenue_lkr"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    daily_revenue,
    x="order_date",
    y="revenue_lkr",
    title="Daily Revenue Trend",
    markers=True,
    labels={
        "order_date": "Order Date",
        "revenue_lkr": "Revenue (LKR)"
    }
)

st.plotly_chart(
    fig3,
    width="stretch"
)

# =========================
# PROFIT BY PRODUCT CATEGORY
# =========================

st.subheader("💹 Profit by Product Category")

category_profit = (
    filtered_df
    .groupby("product_category")["profit_lkr"]
    .sum()
    .reset_index()
    .sort_values(
        "profit_lkr",
        ascending=False
    )
)

fig4 = px.bar(
    category_profit,
    x="product_category",
    y="profit_lkr",
    title="Profit by Product Category",
    labels={
        "profit_lkr": "Profit (LKR)",
        "product_category": "Product Category"
    }
)

st.plotly_chart(
    fig4,
    width="stretch"
)

# =========================
# SALES CHANNEL ANALYSIS
# =========================

st.subheader("🛒 Revenue by Sales Channel")

channel_sales = (
    filtered_df
    .groupby("sales_channel")["revenue_lkr"]
    .sum()
    .reset_index()
    .sort_values(
        "revenue_lkr",
        ascending=False
    )
)

fig5 = px.pie(
    channel_sales,
    names="sales_channel",
    values="revenue_lkr",
    title="Revenue Distribution by Sales Channel",
    hole=0.3
)

st.plotly_chart(
    fig5,
    width="stretch"
)

# =========================
# CUSTOMER SEGMENT ANALYSIS
# =========================

st.subheader("👥 Revenue by Customer Segment")

segment_sales = (
    filtered_df
    .groupby("customer_segment")["revenue_lkr"]
    .sum()
    .reset_index()
    .sort_values(
        "revenue_lkr",
        ascending=False
    )
)

fig6 = px.bar(
    segment_sales,
    x="customer_segment",
    y="revenue_lkr",
    title="Revenue by Customer Segment",
    labels={
        "customer_segment": "Customer Segment",
        "revenue_lkr": "Revenue (LKR)"
    }
)

st.plotly_chart(
    fig6,
    width="stretch"
)

# =========================
# CUSTOMER SEGMENT PROFIT
# =========================

st.subheader("💰 Profit by Customer Segment")

segment_profit = (
    filtered_df
    .groupby("customer_segment")["profit_lkr"]
    .sum()
    .reset_index()
    .sort_values(
        "profit_lkr",
        ascending=False
    )
)

fig7 = px.bar(
    segment_profit,
    x="customer_segment",
    y="profit_lkr",
    title="Profit by Customer Segment",
    labels={
        "customer_segment": "Customer Segment",
        "profit_lkr": "Profit (LKR)"
    }
)

st.plotly_chart(
    fig7,
    width="stretch"
)

# =========================
# PAYMENT METHOD ANALYSIS
# =========================

st.subheader("💳 Revenue by Payment Method")

payment_sales = (
    filtered_df
    .groupby("payment_method")["revenue_lkr"]
    .sum()
    .reset_index()
    .sort_values(
        "revenue_lkr",
        ascending=False
    )
)

fig8 = px.bar(
    payment_sales,
    x="payment_method",
    y="revenue_lkr",
    title="Revenue by Payment Method",
    labels={
        "payment_method": "Payment Method",
        "revenue_lkr": "Revenue (LKR)"
    }
)

st.plotly_chart(
    fig8,
    width="stretch"
)

# =========================
# CUSTOMER RATING ANALYSIS
# =========================

st.subheader("⭐ Customer Rating Analysis")

rating_analysis = (
    filtered_df
    .groupby("customer_rating")
    .size()
    .reset_index(name="order_count")
    .sort_values("customer_rating")
)

fig9 = px.bar(
    rating_analysis,
    x="customer_rating",
    y="order_count",
    title="Orders by Customer Rating",
    labels={
        "customer_rating": "Customer Rating",
        "order_count": "Number of Orders"
    }
)

st.plotly_chart(
    fig9,
    width="stretch"
)

# =========================
# RETURNED ORDERS ANALYSIS
# =========================

st.subheader("🔄 Returned Orders Analysis")

return_analysis = (
    filtered_df
    .groupby("returned")
    .size()
    .reset_index(name="order_count")
)

fig10 = px.pie(
    return_analysis,
    names="returned",
    values="order_count",
    title="Returned vs Non-Returned Orders",
    hole=0.3
)

st.plotly_chart(
    fig10,
    width="stretch"
)

# =========================
# TOP PRODUCTS ANALYSIS
# =========================

st.subheader("🏆 Top 10 Products by Revenue")

top_products = (
    filtered_df
    .groupby("product_name")["revenue_lkr"]
    .sum()
    .reset_index()
    .sort_values(
        "revenue_lkr",
        ascending=False
    )
    .head(10)
)

fig11 = px.bar(
    top_products,
    x="revenue_lkr",
    y="product_name",
    orientation="h",
    title="Top 10 Products by Revenue",
    labels={
        "product_name": "Product",
        "revenue_lkr": "Revenue (LKR)"
    }
)

fig11.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig11,
    width="stretch"
)

# =========================
# PROMOTION ANALYSIS
# =========================

st.subheader("🎯 Revenue by Promotion")

promotion_sales = (
    filtered_df
    .groupby("promotion")["revenue_lkr"]
    .sum()
    .reset_index()
    .sort_values(
        "revenue_lkr",
        ascending=False
    )
)

fig12 = px.bar(
    promotion_sales,
    x="promotion",
    y="revenue_lkr",
    title="Revenue by Promotion",
    labels={
        "promotion": "Promotion",
        "revenue_lkr": "Revenue (LKR)"
    }
)

st.plotly_chart(
    fig12,
    width="stretch"
)

# =========================
# DELIVERY ANALYSIS
# =========================

st.subheader("🚚 Delivery Days Analysis")

delivery_analysis = (
    filtered_df
    .groupby("delivery_days")
    .size()
    .reset_index(name="order_count")
    .sort_values("delivery_days")
)

fig13 = px.bar(
    delivery_analysis,
    x="delivery_days",
    y="order_count",
    title="Orders by Delivery Days",
    labels={
        "delivery_days": "Delivery Days",
        "order_count": "Number of Orders"
    }
)

st.plotly_chart(
    fig13,
    width="stretch"
)

# =========================
# DELIVERY SUMMARY
# =========================

st.subheader("⏱️ Delivery Summary")

if not filtered_df["delivery_days"].dropna().empty:

    average_delivery = filtered_df["delivery_days"].mean()
    fastest_delivery = filtered_df["delivery_days"].min()
    slowest_delivery = filtered_df["delivery_days"].max()

    delivery_col1, delivery_col2, delivery_col3 = st.columns(3)

    delivery_col1.metric(
        "📦 Average Delivery",
        f"{average_delivery:.1f} Days"
    )

    delivery_col2.metric(
        "⚡ Fastest Delivery",
        f"{fastest_delivery:.0f} Day(s)"
    )

    delivery_col3.metric(
        "🐢 Slowest Delivery",
        f"{slowest_delivery:.0f} Day(s)"
    )

else:
    st.warning(
        "No delivery data available for the selected filters."
    )

# =========================
# PROFIT MARGIN ANALYSIS
# =========================

st.subheader("📈 Profit Margin Analysis")

if total_revenue > 0:

    overall_profit_margin = (
        total_profit / total_revenue
    ) * 100

    margin_col1, margin_col2 = st.columns(2)

    margin_col1.metric(
        "📊 Overall Profit Margin",
        f"{overall_profit_margin:.2f}%"
    )

    margin_col2.metric(
        "💵 Profit per Order",
        f"LKR {(total_profit / total_orders):,.2f}"
        if total_orders > 0
        else "LKR 0.00"
    )

else:

    st.warning(
        "No revenue data available for profit margin analysis."
    )

# =========================
# PROFIT MARGIN BY CATEGORY
# =========================

st.subheader("🛍️ Profit Margin by Product Category")

category_margin = (
    filtered_df
    .groupby("product_category")
    .agg(
        revenue_lkr=("revenue_lkr", "sum"),
        profit_lkr=("profit_lkr", "sum")
    )
    .reset_index()
)

category_margin = category_margin[
    category_margin["revenue_lkr"] != 0
]

category_margin["profit_margin_pct"] = (
    category_margin["profit_lkr"]
    / category_margin["revenue_lkr"]
) * 100

category_margin = category_margin.sort_values(
    "profit_margin_pct",
    ascending=False
)

fig14 = px.bar(
    category_margin,
    x="product_category",
    y="profit_margin_pct",
    title="Profit Margin by Product Category",
    labels={
        "product_category": "Product Category",
        "profit_margin_pct": "Profit Margin (%)"
    }
)

st.plotly_chart(
    fig14,
    width="stretch"
)

# =========================
# PROFIT MARGIN BY PROVINCE
# =========================

st.subheader("📍 Profit Margin by Province")

province_margin = (
    filtered_df
    .groupby("province")
    .agg(
        revenue_lkr=("revenue_lkr", "sum"),
        profit_lkr=("profit_lkr", "sum")
    )
    .reset_index()
)

province_margin = province_margin[
    province_margin["revenue_lkr"] != 0
]

province_margin["profit_margin_pct"] = (
    province_margin["profit_lkr"]
    / province_margin["revenue_lkr"]
) * 100

province_margin = province_margin.sort_values(
    "profit_margin_pct",
    ascending=False
)

fig15 = px.bar(
    province_margin,
    x="province",
    y="profit_margin_pct",
    title="Profit Margin by Province",
    labels={
        "province": "Province",
        "profit_margin_pct": "Profit Margin (%)"
    }
)

st.plotly_chart(
    fig15,
    width="stretch"
)

# =========================
# SALES PERFORMANCE SUMMARY
# =========================

st.subheader("📊 Sales Performance Summary")

total_units = filtered_df["units"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

average_rating = filtered_df["customer_rating"].mean()

returned_orders = (
    filtered_df["returned"]
    .astype(str)
    .str.lower()
    .isin(["yes", "true", "1"])
    .sum()
)

return_rate = (
    (returned_orders / total_orders) * 100
    if total_orders > 0
    else 0
)

summary_col1, summary_col2, summary_col3 = st.columns(3)

summary_col1.metric(
    "📦 Total Units Sold",
    f"{total_units:,.0f}"
)

summary_col2.metric(
    "🧾 Average Order Value",
    f"LKR {average_order_value:,.2f}"
)

summary_col3.metric(
    "⭐ Average Customer Rating",
    f"{average_rating:.2f}"
    if pd.notna(average_rating)
    else "N/A"
)

summary_col4, summary_col5, summary_col6 = st.columns(3)

summary_col4.metric(
    "🔄 Returned Orders",
    f"{returned_orders:,}"
)

summary_col5.metric(
    "📉 Return Rate",
    f"{return_rate:.2f}%"
)

# =========================
# BEST PERFORMING PROVINCE
# =========================

if not filtered_df.empty:

    province_performance = (
        filtered_df
        .groupby("province")["revenue_lkr"]
        .sum()
        .sort_values(ascending=False)
    )

    if not province_performance.empty:

        best_province = province_performance.index[0]
        best_province_revenue = province_performance.iloc[0]

        summary_col6.metric(
            "🏆 Best Performing Province",
            best_province,
            f"LKR {best_province_revenue:,.2f}"
        )

# =========================
# SALES PERFORMANCE CHART
# =========================

st.subheader("📈 Sales Performance by Province")

performance_data = (
    filtered_df
    .groupby("province")
    .agg(
        Revenue=("revenue_lkr", "sum"),
        Profit=("profit_lkr", "sum"),
        Units=("units", "sum")
    )
    .reset_index()
)

fig16 = px.bar(
    performance_data,
    x="province",
    y=["Revenue", "Profit"],
    barmode="group",
    title="Sales Performance by Province",
    labels={
        "value": "Amount (LKR)",
        "province": "Province",
        "variable": "Metric"
    }
)

st.plotly_chart(
    fig16,
    width="stretch"
)

# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption(
    "LankaMart Retail Sales Dashboard | CIT308 Data Visualization Project"
)

