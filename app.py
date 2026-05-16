import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from parser import extract_text, parse_sales, parse_excel, parse_csv
from storage import upload_pdf
from database import insert_data, load_data, create_file_metadata, update_file_status
from analysis import *
from model import forecast
from auth import require_authentication, get_user_id, get_user_email, sign_out, init_session_state
from exports import export_to_excel, export_to_csv, export_analytics_report
import uuid

st.set_page_config(
    page_title="Sales Intelligence AI",
    layout="wide",
    page_icon="📊"
)

# Initialize session state
init_session_state()

# Require authentication
require_authentication()

# Get current user
user_id = get_user_id()
user_email = get_user_email()

# ---------- CUSTOM UI ----------

st.markdown(
    """
    <style>
    /* Clean White Background Theme */
    .main {
        background-color: #ffffff;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }

    /* Metric Cards */
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .stMetric label {
        color: #6b7280 !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    /* Headers */
    h1 {
        color: #111827;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    
    h2, h3 {
        color: #374151;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        transition: all 0.3s ease;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        color: #374151;
    }
    
    .stButton > button:hover {
        background-color: #f9fafb;
        border-color: #d1d5db;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f9fafb;
        border-right: 1px solid #e5e7eb;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        width: 100%;
    }
    
    /* Sidebar User Section */
    .sidebar-user-section {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #ffffff;
        border-top: 1px solid #e5e7eb;
        padding: 1rem;
        box-shadow: 0 -2px 8px rgba(0,0,0,0.05);
    }
    
    .user-profile {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem;
        background: #f9fafb;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    
    .user-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 14px;
    }
    
    .user-details {
        flex: 1;
        min-width: 0;
    }
    
    .user-email {
        font-size: 13px;
        font-weight: 600;
        color: #111827;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .user-status {
        font-size: 11px;
        color: #10b981;
        font-weight: 500;
    }
    
    .logout-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.6rem;
        background: #fee2e2;
        color: #dc2626;
        border: 1px solid #fecaca;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .logout-btn:hover {
        background: #fecaca;
        border-color: #fca5a5;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    /* Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }
    
    /* Charts */
    .js-plotly-plot {
        border-radius: 12px;
        background-color: #ffffff;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        min-height: 400px;
    }
    
    .js-plotly-plot .plotly {
        width: 100% !important;
        height: 100% !important;
    }
    
    /* Ensure charts are visible */
    [data-testid="stPlotlyChart"] {
        width: 100%;
        min-height: 400px;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        background-color: #ffffff;
        padding: 1rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Selectbox and inputs */
    .stSelectbox, .stDateInput {
        background-color: #ffffff;
    }
    
    .stSelectbox > div > div, .stDateInput > div > div {
        border-radius: 10px;
        border: 1px solid #d1d5db;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
    }
    
    .stDownloadButton > button:hover {
        background-color: #2563eb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------

st.title("📊 Sales Intelligence Dashboard")

# ---------- SIDEBAR ----------

st.sidebar.header("📁 Upload Sales Files")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF, Excel, or CSV files",
    type=["pdf", "xlsx", "xls", "csv"],
    accept_multiple_files=True,
    help="Supported formats: PDF, Excel (.xlsx, .xls), CSV"
)

if uploaded_files:
    with st.spinner("Processing files..."):
        success_count = 0
        error_count = 0
        
        for uploaded in uploaded_files:
            try:
                file_id = str(uuid.uuid4())
                file_type = uploaded.name.split('.')[-1].lower()
                file_size = uploaded.size
                
                # Create file metadata
                create_file_metadata(file_id, user_id, uploaded.name, file_type, file_size)
                
                # Parse based on file type
                if file_type == 'pdf':
                    uploaded.seek(0)
                    df_new = parse_sales(uploaded)
                    
                    # Upload to storage
                    uploaded.seek(0)
                    file_id_storage, file_url = upload_pdf(uploaded)
                    
                elif file_type in ['xlsx', 'xls']:
                    uploaded.seek(0)
                    df_new = parse_excel(uploaded)
                    
                elif file_type == 'csv':
                    uploaded.seek(0)
                    df_new = parse_csv(uploaded)
                
                else:
                    st.sidebar.error(f"Unsupported file type: {file_type}")
                    continue
                
                # Insert data if extraction successful
                if not df_new.empty:
                    success = insert_data(df_new, file_id, user_id)
                    if success:
                        update_file_status(file_id, 'completed', len(df_new))
                        success_count += 1
                    else:
                        update_file_status(file_id, 'failed', 0, 'Failed to insert data')
                        error_count += 1
                else:
                    update_file_status(file_id, 'failed', 0, 'No data extracted')
                    error_count += 1
                    
            except Exception as e:
                error_count += 1
                st.sidebar.error(f"Error processing {uploaded.name}: {str(e)}")
        
        if success_count > 0:
            st.sidebar.success(f"✅ Successfully processed {success_count} file(s)")
        if error_count > 0:
            st.sidebar.warning(f"⚠️ Failed to process {error_count} file(s)")

# ---------- LOAD DATABASE ----------

_df = load_data(user_id)

if _df.empty:
    st.info("📤 Upload files to begin analysis")
    st.info("👆 Use the file uploader in the sidebar to get started!")
    st.stop()

_df = prepare(_df)

# ---------- EXPORT SECTION ----------

st.sidebar.markdown("---")
st.sidebar.header("📥 Export Data")

if st.sidebar.button("📊 Export to Excel", use_container_width=True):
    excel_file = export_analytics_report(_df)
    st.sidebar.download_button(
        label="⬇️ Download Excel Report",
        data=excel_file,
        file_name=f"sales_report_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if st.sidebar.button("📄 Export to CSV", use_container_width=True):
    csv_data = export_to_csv(_df)
    st.sidebar.download_button(
        label="⬇️ Download CSV",
        data=csv_data,
        file_name=f"sales_data_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# ---------- FILTERS ----------

st.sidebar.header("Filters")

min_date = _df["invoice_date"].min()
max_date = _df["invoice_date"].max()

selected_dates = st.sidebar.date_input(
    "Date Range",
    [min_date, max_date]
)

categories = ["All"] + sorted(_df["category"].dropna().unique().tolist())

selected_category = st.sidebar.selectbox(
    "Category",
    categories
)

customers = ["All"] + sorted(_df["customer_name"].dropna().unique().tolist())

selected_customer = st.sidebar.selectbox(
    "Customer",
    customers
)

# ---------- USER PROFILE AT BOTTOM ----------

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Account")

# Get user initials for avatar
user_initials = "".join([word[0].upper() for word in user_email.split('@')[0].split('.')[:2]]) if user_email else "U"

st.sidebar.markdown(f"""
<div class="user-profile">
    <div class="user-avatar">{user_initials}</div>
    <div class="user-details">
        <div class="user-email">{user_email}</div>
        <div class="user-status">● Online</div>
    </div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout", key="logout_btn", use_container_width=True):
    success, message = sign_out()
    if success:
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.user_id = None
        st.rerun()

# ---------- APPLY FILTERS ----------

start_date = pd.to_datetime(selected_dates[0])
end_date = pd.to_datetime(selected_dates[1])

filtered_df = _df[
    (_df["invoice_date"] >= start_date) &
    (_df["invoice_date"] <= end_date)
]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]

if selected_customer != "All":
    filtered_df = filtered_df[
        filtered_df["customer_name"] == selected_customer
    ]

# ---------- KPIs ----------

revenue = filtered_df["revenue"].sum()
quantity = filtered_df["quantity"].sum()
products = filtered_df["product_name"].nunique()
customers_count = filtered_df["customer_name"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Revenue", f"₹{int(revenue):,}")
c2.metric("Quantity Sold", int(quantity))
c3.metric("Products", products)
c4.metric("Customers", customers_count)

# ---------- REVENUE TREND ----------

st.subheader("Revenue Trend")

trend = revenue_trend(filtered_df)

fig = px.area(
    trend,
    x="invoice_date",
    y="revenue",
    title="Daily Revenue"
)

st.plotly_chart(fig, use_container_width=True)

# ---------- TOP PRODUCTS ----------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Top Products")

    tp = top_products(filtered_df).head(10)

    fig = px.bar(
        tp,
        orientation="h",
        title="Highest Revenue Products"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("Category Contribution")

    tc = top_categories(filtered_df)

    fig = px.pie(
        values=tc.values,
        names=tc.index,
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------- CUSTOMER ANALYSIS ----------

st.subheader("Top Customers")

cust = top_customers(filtered_df).head(10)

fig = px.bar(
    cust,
    orientation="h"
)

st.plotly_chart(fig, use_container_width=True)

# ---------- INVENTORY RISK ----------

st.subheader("Low Movement Products")

st.dataframe(
    inventory_risk(filtered_df),
    use_container_width=True
)

# ---------- BUSINESS INSIGHTS ----------

st.subheader("AI Business Insights")

insights = business_insights(filtered_df)

for i in insights:

    st.success(i)

# ---------- SMART INSIGHTS ----------

st.subheader("Strategic Recommendations")

best_product = (
    filtered_df.groupby("product_name")["revenue"]
    .sum()
    .idxmax()
)

worst_products = (
    filtered_df.groupby("product_name")["revenue"]
    .sum()
    .sort_values()
    .head(3)
    .index
    .tolist()
)

repeat_customers = (
    filtered_df.groupby("customer_name")
    .size()
    .sort_values(ascending=False)
    .head(5)
)

st.info(
    f"Focus marketing on your best-selling product: {best_product}"
)

st.warning(
    f"Consider discounting or replacing low-performing products: {', '.join(worst_products)}"
)

st.success(
    f"Top repeat customers detected: {', '.join(repeat_customers.index.tolist())}"
)

# ---------- ANOMALY DETECTION ----------

st.subheader("Sales Anomaly Detection")

anomalies = anomaly_detection(filtered_df)

if not anomalies.empty:

    fig = px.scatter(
        anomalies,
        x="invoice_date",
        y="revenue",
        title="Unusual Revenue Spikes/Drops"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(anomalies)

else:

    st.success("No unusual anomalies detected")

# ---------- FORECAST ----------

st.subheader("7-Day Revenue Forecast")

preds = forecast(filtered_df)

if not preds.empty:

    fig = px.line(
        preds,
        x="Day",
        y="Predicted Revenue",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------- WEEKLY SALES ----------

    st.subheader("Weekly Sales")

    weekly = weekly_sales(filtered_df)

    st.bar_chart(
        weekly.set_index("week")
    )

    # ---------- MONTHLY SALES ----------

    st.subheader("Monthly Sales")

    monthly = monthly_sales(filtered_df)

    st.bar_chart(
        monthly.set_index("month")
    )

    # ---------- WEEKDAY PERFORMANCE ----------

    st.subheader("Sales by Weekday")

    weekday = weekday_sales(filtered_df)

    st.bar_chart(weekday)

    st.dataframe(
        preds,
        use_container_width=True
    )

# ---------- BUSINESS PERFORMANCE METRICS ----------

st.markdown("---")
st.header("📈 Business Performance Metrics")

# Growth Rate Analysis
st.subheader("Growth Analysis")
growth_metrics = growth_rate_analysis(filtered_df)

if growth_metrics:
    col1, col2, col3 = st.columns(3)

    # FIX: use period_label from growth_rate_analysis so the metric title
    # correctly says "Day-over-Day" when data spans < 2 months
    period_label = growth_metrics.get("period_label", "Month-over-Month")
    
    with col1:
        mom_growth = growth_metrics.get("month_over_month", 0)
        st.metric(
            f"{period_label} Growth",
            f"{mom_growth:+.1f}%",
            delta=f"{mom_growth:.1f}%"
        )
    
    with col2:
        overall_growth = growth_metrics.get("overall_growth", 0)
        st.metric(
            "Overall Growth",
            f"{overall_growth:+.1f}%",
            delta=f"{overall_growth:.1f}%"
        )
    
    with col3:
        periods = growth_metrics.get("months_analyzed", 0)
        period_count_label = "Days Analyzed" if "Day" in period_label else "Months Analyzed"
        st.metric(period_count_label, periods)
    
    st.info(f"📊 Revenue grew from ₹{growth_metrics.get('first_month_revenue', 0):,} to ₹{growth_metrics.get('last_month_revenue', 0):,}")

# Customer Retention
st.subheader("Customer Retention Metrics")
retention_metrics = customer_retention_rate(filtered_df)

if retention_metrics:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Customers",
            retention_metrics.get("total_customers", 0)
        )
    
    with col2:
        st.metric(
            "Repeat Customers",
            retention_metrics.get("repeat_customers", 0)
        )
    
    with col3:
        retention_rate = retention_metrics.get("retention_rate", 0)
        st.metric(
            "Retention Rate",
            f"{retention_rate:.1f}%",
            delta=f"{retention_rate:.1f}%" if retention_rate > 50 else f"-{100-retention_rate:.1f}%"
        )
    
    with col4:
        avg_purchases = retention_metrics.get("avg_purchases_per_customer", 0)
        st.metric(
            "Avg Purchases/Customer",
            f"{avg_purchases:.1f}"
        )

    # FIX: show data-volume caveat instead of misleading churn warning
    # when fewer than 30 days of data are available
    if retention_metrics.get("data_warning"):
        days = retention_metrics.get("date_range_days", 0)
        st.info(
            f"ℹ️ Retention is based on only **{days} day(s)** of data. "
            "A customer counts as 'repeat' only if they purchased on multiple days "
            "within this dataset. Upload 30+ days of sales history for a meaningful retention rate."
        )
    else:
        if retention_rate >= 70:
            st.success(f"🎉 Excellent! {retention_rate:.1f}% of your customers are returning - this shows strong customer loyalty!")
        elif retention_rate >= 50:
            st.info(f"👍 Good retention rate of {retention_rate:.1f}%. Consider loyalty programs to improve further.")
        else:
            st.warning(f"⚠️ Retention rate is {retention_rate:.1f}%. Focus on customer satisfaction and follow-up strategies.")

# ---------- PROFIT ANALYSIS ----------

st.markdown("---")
st.subheader("💰 Profit Margin Analysis")

st.info("📝 Note: Profit estimates assume 60% cost of goods. Adjust this in your business settings for accurate calculations.")

profit_df = profit_margin_analysis(filtered_df)

if not profit_df.empty:
    # Show top 10 most profitable products
    top_profit = profit_df.head(10)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Revenue',
        x=top_profit['Product'],
        y=top_profit['Revenue'],
        marker_color='lightblue'
    ))
    fig.add_trace(go.Bar(
        name='Estimated Profit',
        x=top_profit['Product'],
        y=top_profit['Estimated Profit'],
        marker_color='green'
    ))
    
    fig.update_layout(
        title='Top 10 Products by Profitability',
        barmode='group',
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show detailed table
    with st.expander("📊 View Detailed Profit Analysis"):
        st.dataframe(
            profit_df.style.format({
                'Revenue': '₹{:,.0f}',
                'Estimated Cost': '₹{:,.0f}',
                'Estimated Profit': '₹{:,.0f}',
                'Profit Margin %': '{:.2f}%'
            }),
            use_container_width=True
        )

# ---------- SALES VELOCITY ----------

st.markdown("---")
st.subheader("⚡ Sales Velocity - How Fast Products Sell")

velocity_df = sales_velocity(filtered_df)

if not velocity_df.empty:
    # Show top performers
    top_velocity = velocity_df.head(10)
    
    fig = px.bar(
        top_velocity,
        x='Product',
        y='Units Per Day',
        title='Fastest Moving Products (Units per Day)',
        color='Revenue Per Day',
        color_continuous_scale='Greens'
    )
    fig.update_layout(xaxis_tickangle=-45)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    fastest_product = velocity_df.iloc[0]['Product']
    fastest_rate = velocity_df.iloc[0]['Units Per Day']
    st.success(f"🏃 Fastest mover: **{fastest_product}** sells {fastest_rate:.1f} units per day on average")
    
    with st.expander("📊 View Complete Sales Velocity Data"):
        st.dataframe(
            velocity_df.style.format({
                'Total Quantity': '{:.0f}',
                'Total Revenue': '₹{:,.0f}',
                'Units Per Day': '{:.2f}',
                'Revenue Per Day': '₹{:,.2f}'
            }),
            use_container_width=True
        )

# ---------- CUSTOMER LIFETIME VALUE (FIXED) ----------

st.markdown("---")
st.subheader("💎 Customer Lifetime Value (CLV)")

# FIX: customer_lifetime_value now returns a dict, not a DataFrame.
# It refuses to project when data spans < 30 days to avoid nonsensical
# figures like ₹89M total CLV from just 2 days of sales data.
clv_result     = customer_lifetime_value(filtered_df)
clv_df         = clv_result.get("df", pd.DataFrame())
clv_sufficient = clv_result.get("sufficient_data", False)
clv_days       = clv_result.get("date_range_days", 0)

if not clv_df.empty:

    if not clv_sufficient:
        st.warning(
            f"⚠️ Only **{clv_days} day(s)** of data available. "
            "CLV projection requires at least **30 days** of sales history to be meaningful. "
            "Showing **observed revenue per customer** instead of a projected lifetime value."
        )

    top_clv = clv_df.head(10)

    fig = px.bar(
        top_clv,
        x='Customer',
        y='Total Revenue',
        title='Top 10 Customers by Revenue' if not clv_sufficient else 'Top 10 Customers by Lifetime Value',
        color='Total Revenue',
        color_continuous_scale='Blues',
        labels={'Total Revenue': 'Revenue (₹)'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Key insights
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Revenue (All Customers)",
            f"₹{int(clv_df['Total Revenue'].sum()):,}"
        )

    with col2:
        st.metric(
            "Avg Revenue per Customer",
            f"₹{int(clv_df['Total Revenue'].mean()):,}"
        )

    if clv_sufficient:
        st.info(
            f"💡 Your top customer has an estimated 12-month lifetime value of "
            f"₹{int(clv_df.iloc[0]['Estimated CLV (12-month)']):,}. "
            "Focus on maintaining these high-value relationships!"
        )
    else:
        st.info(
            f"💡 Your top customer by revenue is **{clv_df.iloc[0]['Customer']}** "
            f"with ₹{int(clv_df.iloc[0]['Total Revenue']):,} in this period. "
            "Upload more historical data to unlock CLV projections."
        )

    with st.expander("📊 View Complete CLV Analysis"):
        fmt = {
            'Total Revenue':   '₹{:,.0f}',
            'Avg Order Value': '₹{:,.0f}',
        }
        if clv_sufficient:
            fmt['Estimated CLV (12-month)'] = '₹{:,.0f}'
        st.dataframe(
            clv_df.style.format(fmt),
            use_container_width=True
        )

# ---------- PRODUCT BUNDLING OPPORTUNITIES ----------

st.markdown("---")
st.subheader("🎁 Product Bundling Opportunities")

bundling_df = product_bundling_opportunities(filtered_df)

if not bundling_df.empty:
    st.write("Products frequently bought together - consider creating bundle offers:")
    
    # Show top 10 pairs
    top_bundles = bundling_df.head(10)
    
    for idx, row in top_bundles.iterrows():
        st.write(f"🔗 **{row['Product A']}** + **{row['Product B']}** → Bought together {row['Times Bought Together']} times")
    
    st.success("💡 Create combo offers for these product pairs to increase average order value!")
    
    with st.expander("📊 View All Bundling Opportunities"):
        st.dataframe(bundling_df, use_container_width=True)
else:
    st.info("📦 No bundling patterns detected yet. This analysis requires multiple products per transaction.")

# ---------- SEASONAL TRENDS ----------

st.markdown("---")
st.subheader("🌤️ Seasonal Sales Patterns")

seasonal_df = seasonal_trends(filtered_df)

if not seasonal_df.empty:
    fig = px.bar(
        seasonal_df,
        x='Month',
        y='Revenue',
        color='Quarter',
        title='Revenue by Month and Quarter',
        color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Find best and worst months
    best_month = seasonal_df.loc[seasonal_df['Revenue'].idxmax()]
    worst_month = seasonal_df.loc[seasonal_df['Revenue'].idxmin()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"📈 Best Month: **{best_month['Month']}** (Q{best_month['Quarter']}) with ₹{int(best_month['Revenue']):,}")
    
    with col2:
        st.warning(f"📉 Slowest Month: **{worst_month['Month']}** (Q{worst_month['Quarter']}) with ₹{int(worst_month['Revenue']):,}")

    # FIX: add honest note when only one month of data exists
    if len(seasonal_df) == 1:
        st.info("ℹ️ Only one month of data available. Upload more months to see meaningful seasonal patterns.")
    else:
        st.info("💡 Plan inventory and marketing campaigns based on these seasonal patterns!")

# ---------- PAYMENT TERMS ANALYSIS ----------

if "payment_terms" in filtered_df.columns:
    st.markdown("---")
    st.subheader("💳 Payment Terms Analysis")
    
    payment_df = payment_terms_analysis(filtered_df)
    
    if not payment_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                payment_df,
                values='Total Revenue',
                names='Payment Terms',
                title='Revenue Distribution by Payment Terms'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                payment_df,
                x='Payment Terms',
                y='Avg Transaction',
                title='Average Transaction Value by Payment Terms',
                color='Avg Transaction',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(
            payment_df.style.format({
                'Total Revenue': '₹{:,.0f}',
                'Avg Transaction': '₹{:,.0f}',
                '% of Total Revenue': '{:.2f}%'
            }),
            use_container_width=True
        )

# ---------- CUSTOMER SEGMENTATION ----------

st.markdown("---")
st.subheader("👥 Customer Segmentation (RFM Analysis)")

rfm_df = customer_segmentation(filtered_df)

if not rfm_df.empty:
    # Count customers by segment
    segment_counts = rfm_df['Segment'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title='Customer Segments Distribution',
            color_discrete_sequence=['#10b981', '#3b82f6', '#ef4444']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue by segment
        segment_revenue = rfm_df.groupby('Segment')['Monetary Value'].sum()
        fig = px.bar(
            x=segment_revenue.index,
            y=segment_revenue.values,
            title='Revenue by Customer Segment',
            labels={'x': 'Segment', 'y': 'Revenue'},
            color=segment_revenue.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Segment insights
    vip_count = segment_counts.get('VIP', 0)
    at_risk_count = segment_counts.get('At Risk', 0)
    
    if vip_count > 0:
        st.success(f"⭐ You have {vip_count} VIP customers! These are your most valuable - keep them happy!")
    
    if at_risk_count > 0:
        st.warning(f"⚠️ {at_risk_count} customers are at risk of churning. Reach out with special offers or check-ins!")
    
    with st.expander("📊 View Detailed Customer Segmentation"):
        st.dataframe(
            rfm_df.style.format({
                'Monetary Value': '₹{:,.0f}'
            }),
            use_container_width=True
        )
        
        st.markdown("""
        **Segment Definitions:**
        - **VIP**: High frequency and high spending customers - your best customers
        - **At Risk**: Haven't purchased recently - may be losing interest
        - **Regular**: Steady customers with moderate activity
        """)