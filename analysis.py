"""
Analysis module for Sales Intelligence AI
Provides comprehensive analytics and insights
"""
import pandas as pd
import numpy as np
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Preparation
# ---------------------------------------------------------------------------

def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare dataframe with additional time-based columns.
    """
    if df.empty:
        return df

    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["month"] = df["invoice_date"].dt.strftime("%Y-%m")
    df["week"] = df["invoice_date"].dt.isocalendar().week
    df["day"] = df["invoice_date"].dt.day_name()

    return df


# ---------------------------------------------------------------------------
# Basic aggregations (all correct — unchanged)
# ---------------------------------------------------------------------------

def revenue_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily revenue trend."""
    if df.empty:
        return pd.DataFrame()
    return df.groupby("invoice_date")["revenue"].sum().reset_index()


def weekly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate weekly sales."""
    if df.empty:
        return pd.DataFrame()
    return df.groupby("week")["revenue"].sum().reset_index()


def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly sales."""
    if df.empty:
        return pd.DataFrame()
    return df.groupby("month")["revenue"].sum().reset_index()


def top_products(df: pd.DataFrame) -> pd.Series:
    """Get top products by revenue."""
    if df.empty:
        return pd.Series()
    return df.groupby("product_name")["revenue"].sum().sort_values(ascending=False)


def top_categories(df: pd.DataFrame) -> pd.Series:
    """Get top categories by revenue."""
    if df.empty or "category" not in df.columns:
        return pd.Series()
    return df.groupby("category")["revenue"].sum().sort_values(ascending=False)


def top_customers(df: pd.DataFrame) -> pd.Series:
    """Get top customers by revenue."""
    if df.empty or "customer_name" not in df.columns:
        return pd.Series()
    df_filtered = df[df["customer_name"].notna()]
    if df_filtered.empty:
        return pd.Series()
    return df_filtered.groupby("customer_name")["revenue"].sum().sort_values(ascending=False)


def inventory_risk(df: pd.DataFrame, threshold: int = 5) -> pd.DataFrame:
    """Identify low-movement products (inventory risk)."""
    if df.empty:
        return pd.DataFrame()

    product_movement = (
        df.groupby("product_name")
        .agg({"quantity": "sum", "revenue": "sum", "invoice_date": "max"})
        .reset_index()
    )
    product_movement.columns = ["Product", "Total Quantity", "Total Revenue", "Last Sale Date"]
    low_movement = product_movement[product_movement["Total Quantity"] <= threshold]
    return low_movement.sort_values("Total Quantity")


def product_quantity(df: pd.DataFrame) -> pd.Series:
    """Get product quantities sold."""
    if df.empty:
        return pd.Series()
    return df.groupby("product_name")["quantity"].sum().sort_values(ascending=False)


def weekday_sales(df: pd.DataFrame) -> pd.Series:
    """Calculate sales by weekday."""
    if df.empty or "day" not in df.columns:
        return pd.Series()
    return (
        df.groupby("day")["revenue"]
        .sum()
        .reindex(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            fill_value=0,
        )
    )


# ---------------------------------------------------------------------------
# FIX 1 — business_insights: day-over-day growth, not row-slice comparison
# ---------------------------------------------------------------------------

def business_insights(df: pd.DataFrame) -> List[str]:
    """
    Generate business insights.

    FIX: growth now compares actual daily totals (day-over-day) instead of
    comparing arbitrary head/tail row slices, which was meaningless.
    """
    insights = []

    if df.empty:
        return ["No data available for analysis"]

    try:
        total_revenue = int(df["revenue"].sum())
        insights.append(f"💰 Total revenue generated: ₹{total_revenue:,}")

        if "product_name" in df.columns:
            top_product = df.groupby("product_name")["revenue"].sum().idxmax()
            insights.append(f"🏆 Best selling product: {top_product}")

        if "day" in df.columns:
            highest_day = df.groupby("day")["revenue"].sum().idxmax()
            insights.append(f"📅 Highest sales occur on: {highest_day}")

        avg_order = int(df["revenue"].mean())
        insights.append(f"📊 Average transaction value: ₹{avg_order:,}")

        # FIX: compare daily totals, not arbitrary row head/tail slices
        daily_rev = df.groupby("invoice_date")["revenue"].sum().sort_index()

        if len(daily_rev) >= 2:
            prev_day_rev = daily_rev.iloc[-2]
            last_day_rev = daily_rev.iloc[-1]
            prev_date = daily_rev.index[-2].strftime("%d %b")
            last_date = daily_rev.index[-1].strftime("%d %b")

            if prev_day_rev > 0:
                growth = ((last_day_rev - prev_day_rev) / prev_day_rev) * 100
                if growth >= 0:
                    insights.append(
                        f"📈 Revenue grew by {growth:.1f}% from {prev_date} "
                        f"(₹{int(prev_day_rev):,}) to {last_date} (₹{int(last_day_rev):,})"
                    )
                else:
                    insights.append(
                        f"📉 Revenue declined by {abs(growth):.1f}% from {prev_date} "
                        f"(₹{int(prev_day_rev):,}) to {last_date} (₹{int(last_day_rev):,})"
                    )
        elif len(daily_rev) == 1:
            insights.append(
                f"📅 Single day of data ({daily_rev.index[0].strftime('%d %b')}). "
                "Upload more days to see growth trends."
            )

        if "customer_name" in df.columns:
            unique_customers = df["customer_name"].nunique()
            insights.append(f"👥 Serving {unique_customers} unique customers")

    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        insights.append("⚠️ Unable to generate some insights")

    return insights


# ---------------------------------------------------------------------------
# FIX 2 — anomaly_detection: check number of days, not number of rows
# ---------------------------------------------------------------------------

def anomaly_detection(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    """
    Detect anomalies in sales data using statistical methods.

    FIX: the original check (len(df) < 10) tested row count, so it always
    returned empty for small datasets even with many days. Now we require at
    least 10 *daily* data points (i.e. 10 distinct days of sales).
    """
    if df.empty:
        return pd.DataFrame()

    try:
        daily_revenue = df.groupby("invoice_date")["revenue"].sum().reset_index()

        # Need at least 10 days to make z-score meaningful
        if len(daily_revenue) < 10:
            return pd.DataFrame()

        mean_rev = daily_revenue["revenue"].mean()
        std_rev = daily_revenue["revenue"].std()

        if std_rev == 0:
            return pd.DataFrame()

        daily_revenue["z_score"] = (daily_revenue["revenue"] - mean_rev) / std_rev
        anomalies = daily_revenue[abs(daily_revenue["z_score"]) > threshold]

        return anomalies[["invoice_date", "revenue"]].sort_values("invoice_date")

    except Exception as e:
        logger.error(f"Error detecting anomalies: {str(e)}")
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# FIX 3 — growth_rate_analysis: day-over-day when data spans < 2 months
# ---------------------------------------------------------------------------

def growth_rate_analysis(df: pd.DataFrame) -> dict:
    """
    Calculate growth rates.

    FIX: the original function grouped by month, so all data within the same
    calendar month produced a single row → 0% growth always shown. Now we
    detect whether data spans multiple months and fall back to day-over-day
    comparison when it doesn't.
    """
    if df.empty or len(df) < 2:
        return {}

    try:
        df_sorted = df.sort_values("invoice_date")
        monthly_revenue = df_sorted.groupby("month")["revenue"].sum().sort_index()

        if len(monthly_revenue) >= 2:
            # Normal month-over-month comparison
            current  = monthly_revenue.iloc[-1]
            previous = monthly_revenue.iloc[-2]
            mom_growth     = ((current - previous) / previous * 100) if previous > 0 else 0
            overall_growth = ((current - monthly_revenue.iloc[0]) / monthly_revenue.iloc[0] * 100) \
                             if monthly_revenue.iloc[0] > 0 else 0
            period_label   = "Month-over-Month"
            first_rev      = int(monthly_revenue.iloc[0])
            last_rev       = int(current)
            periods        = len(monthly_revenue)

        else:
            # Fall back to day-over-day when all data is within one month
            daily_revenue = df_sorted.groupby("invoice_date")["revenue"].sum().sort_index()

            if len(daily_revenue) >= 2:
                current  = daily_revenue.iloc[-1]
                previous = daily_revenue.iloc[-2]
                mom_growth     = ((current - previous) / previous * 100) if previous > 0 else 0
                overall_growth = ((current - daily_revenue.iloc[0]) / daily_revenue.iloc[0] * 100) \
                                 if daily_revenue.iloc[0] > 0 else 0
                period_label   = "Day-over-Day"
                first_rev      = int(daily_revenue.iloc[0])
                last_rev       = int(current)
                periods        = len(daily_revenue)
            else:
                return {}

        return {
            "month_over_month":    round(mom_growth, 2),
            "overall_growth":      round(overall_growth, 2),
            "months_analyzed":     periods,
            "period_label":        period_label,
            "first_month_revenue": first_rev,
            "last_month_revenue":  last_rev,
        }

    except Exception as e:
        logger.error(f"Error calculating growth rate: {str(e)}")
        return {}


# ---------------------------------------------------------------------------
# FIX 4 — customer_retention_rate: honest note when data is < 30 days
# ---------------------------------------------------------------------------

def customer_retention_rate(df: pd.DataFrame) -> dict:
    """
    Calculate customer retention metrics.

    FIX: with only 1–2 days of data almost no customer will have a repeat
    purchase, so retention always showed ~0%. The function now adds a
    'data_warning' key when the date range is under 30 days so app.py can
    surface the caveat rather than showing a misleading 0%.
    """
    if df.empty or "customer_name" not in df.columns:
        return {}

    try:
        df_filtered = df[df["customer_name"].notna()].copy()
        if df_filtered.empty:
            return {}

        date_range_days = (
            df_filtered["invoice_date"].max() - df_filtered["invoice_date"].min()
        ).days + 1

        customer_purchases = df_filtered.groupby("customer_name")["invoice_number"].nunique()

        total_customers    = len(customer_purchases)
        repeat_customers   = len(customer_purchases[customer_purchases > 1])
        one_time_customers = len(customer_purchases[customer_purchases == 1])
        retention_rate     = (repeat_customers / total_customers * 100) if total_customers > 0 else 0

        result = {
            "total_customers":           total_customers,
            "repeat_customers":          repeat_customers,
            "one_time_customers":        one_time_customers,
            "retention_rate":            round(retention_rate, 2),
            "avg_purchases_per_customer": round(customer_purchases.mean(), 2),
            "data_warning":              date_range_days < 30,
            "date_range_days":           date_range_days,
        }

        return result

    except Exception as e:
        logger.error(f"Error calculating retention rate: {str(e)}")
        return {}


# ---------------------------------------------------------------------------
# FIX 5 — customer_lifetime_value: guard against 1-day tenure inflating CLV
# ---------------------------------------------------------------------------

def customer_lifetime_value(df: pd.DataFrame) -> dict:
    """
    Calculate Customer Lifetime Value (CLV) metrics.

    FIX: CLV projection requires a meaningful observation window (≥ 30 days)
    to produce reliable frequency estimates. With < 30 days of data, any
    projection (orders/day × 365) is wildly inflated because you're
    extrapolating from a single burst of activity.

    When data spans < 30 days we return observed totals only — no projection.
    The 'sufficient_data' key tells app.py which mode we're in so it can
    show the correct UI and caveat.

    Returns a dict with keys:
        sufficient_data  bool   — True if ≥ 30 days, False otherwise
        date_range_days  int    — actual days spanned
        df               DataFrame — per-customer stats
    """
    empty = {"sufficient_data": False, "date_range_days": 0, "df": pd.DataFrame()}

    if df.empty or "customer_name" not in df.columns:
        return empty

    try:
        df_filtered = df[df["customer_name"].notna()].copy()
        if df_filtered.empty:
            return empty

        date_range_days = (
            df_filtered["invoice_date"].max() - df_filtered["invoice_date"].min()
        ).days + 1

        clv = df_filtered.groupby("customer_name").agg(
            Total_Revenue  =("revenue",       "sum"),
            Avg_Order_Value=("revenue",       "mean"),
            Num_Orders     =("invoice_number","count"),
            First_Purchase =("invoice_date",  "min"),
            Last_Purchase  =("invoice_date",  "max"),
        ).reset_index()

        clv.columns = [
            "Customer", "Total Revenue", "Avg Order Value",
            "Number of Orders", "First Purchase", "Last Purchase",
        ]

        clv["Customer Tenure (days)"] = (
            clv["Last Purchase"] - clv["First Purchase"]
        ).dt.days + 1

        sufficient = date_range_days >= 30

        if sufficient:
            # Only project when we have enough history
            clv["Purchase Frequency (monthly)"] = (
                clv["Number of Orders"]
                / (clv["Customer Tenure (days)"] / 30)
            ).round(2)
            clv["Estimated CLV (12-month)"] = (
                clv["Avg Order Value"]
                * clv["Purchase Frequency (monthly)"]
                * 12
            ).round(2)
            clv["CLV Basis"] = "Projected (12-month)"
            sort_col = "Estimated CLV (12-month)"
        else:
            # Not enough data — show observed revenue only, no projection
            clv["Estimated CLV (12-month)"] = clv["Total Revenue"]
            clv["CLV Basis"] = "Observed revenue only (insufficient history for projection)"
            sort_col = "Total Revenue"

        clv = clv.sort_values(sort_col, ascending=False)

        return {
            "sufficient_data":  sufficient,
            "date_range_days":  date_range_days,
            "df":               clv,
        }

    except Exception as e:
        logger.error(f"Error calculating CLV: {str(e)}")
        return empty


# ---------------------------------------------------------------------------
# Other functions (correct — unchanged)
# ---------------------------------------------------------------------------

def customer_segmentation(df: pd.DataFrame) -> pd.DataFrame:
    """Perform RFM analysis for customer segmentation."""
    if df.empty or "customer_name" not in df.columns:
        return pd.DataFrame()

    try:
        df_filtered = df[df["customer_name"].notna()].copy()
        if df_filtered.empty:
            return pd.DataFrame()

        max_date = df_filtered["invoice_date"].max()

        rfm = df_filtered.groupby("customer_name").agg({
            "invoice_date":   lambda x: (max_date - x.max()).days,
            "invoice_number": "count",
            "revenue":        "sum",
        }).reset_index()

        rfm.columns = ["Customer", "Recency (days)", "Frequency", "Monetary Value"]

        rfm["Segment"] = "Regular"
        rfm.loc[
            (rfm["Frequency"]       >= rfm["Frequency"].quantile(0.75)) &
            (rfm["Monetary Value"]  >= rfm["Monetary Value"].quantile(0.75)),
            "Segment"
        ] = "VIP"
        rfm.loc[
            rfm["Recency (days)"] > rfm["Recency (days)"].quantile(0.75),
            "Segment"
        ] = "At Risk"

        return rfm.sort_values("Monetary Value", ascending=False)

    except Exception as e:
        logger.error(f"Error in customer segmentation: {str(e)}")
        return pd.DataFrame()


def profit_margin_analysis(df: pd.DataFrame, cost_percentage: float = 0.6) -> pd.DataFrame:
    """Analyze profit margins by product."""
    if df.empty or "product_name" not in df.columns:
        return pd.DataFrame()

    try:
        profit_analysis = df.groupby("product_name").agg(
            {"revenue": "sum", "quantity": "sum"}
        ).reset_index()

        profit_analysis["Estimated Cost"]   = profit_analysis["revenue"] * cost_percentage
        profit_analysis["Estimated Profit"] = profit_analysis["revenue"] - profit_analysis["Estimated Cost"]
        profit_analysis["Profit Margin %"]  = (
            profit_analysis["Estimated Profit"] / profit_analysis["revenue"] * 100
        ).round(2)

        profit_analysis.columns = [
            "Product", "Revenue", "Quantity",
            "Estimated Cost", "Estimated Profit", "Profit Margin %",
        ]

        return profit_analysis.sort_values("Estimated Profit", ascending=False)

    except Exception as e:
        logger.error(f"Error in profit margin analysis: {str(e)}")
        return pd.DataFrame()


def sales_velocity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate how fast products are selling (units per day).

    Note: with only 1–2 days of data, "Units Per Day" equals the total
    quantity sold in that single day — mathematically correct but should be
    read as a snapshot rate, not a long-run average.
    """
    if df.empty or "product_name" not in df.columns:
        return pd.DataFrame()

    try:
        product_stats = df.groupby("product_name").agg(
            Total_Quantity=("quantity",     "sum"),
            First_Sale    =("invoice_date", "min"),
            Last_Sale     =("invoice_date", "max"),
            Total_Revenue =("revenue",      "sum"),
        ).reset_index()

        product_stats.columns = [
            "Product", "Total Quantity", "First Sale", "Last Sale", "Total Revenue",
        ]

        product_stats["Days Active"] = (
            product_stats["Last Sale"] - product_stats["First Sale"]
        ).dt.days + 1

        product_stats["Units Per Day"]   = (
            product_stats["Total Quantity"] / product_stats["Days Active"]
        ).round(2)

        product_stats["Revenue Per Day"] = (
            product_stats["Total Revenue"] / product_stats["Days Active"]
        ).round(2)

        return product_stats.sort_values("Units Per Day", ascending=False)

    except Exception as e:
        logger.error(f"Error calculating sales velocity: {str(e)}")
        return pd.DataFrame()


def seasonal_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Identify seasonal patterns in sales."""
    if df.empty:
        return pd.DataFrame()

    try:
        df_copy = df.copy()
        df_copy["Month Name"] = df_copy["invoice_date"].dt.strftime("%B")
        df_copy["Quarter"]    = df_copy["invoice_date"].dt.quarter

        seasonal = df_copy.groupby(["Quarter", "Month Name"]).agg(
            {"revenue": "sum", "quantity": "sum"}
        ).reset_index()

        seasonal.columns = ["Quarter", "Month", "Revenue", "Quantity"]
        return seasonal.sort_values(["Quarter", "Revenue"], ascending=[True, False])

    except Exception as e:
        logger.error(f"Error analyzing seasonal trends: {str(e)}")
        return pd.DataFrame()


def product_bundling_opportunities(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify products frequently bought together (co-occurrence per invoice).

    FIX: the same product can appear on multiple line items within one invoice
    (e.g. different size runs of the same chappal). The old code treated each
    line item as a separate entry, causing a product to pair with itself.
    We now deduplicate products per invoice before finding pairs, so only
    genuinely distinct products are counted as co-purchased.

    Pairs are always stored with Product A < Product B (alphabetically) so
    (A, B) and (B, A) are never double-counted.
    """
    if df.empty or "invoice_number" not in df.columns:
        return pd.DataFrame()

    try:
        # Deduplicate: one row per (invoice, product) — removes self-pairs
        invoice_products = (
            df[["invoice_number", "product_name"]]
            .drop_duplicates()
            .groupby("invoice_number")["product_name"]
            .apply(list)
            .reset_index()
        )

        product_pairs = []
        for products in invoice_products["product_name"]:
            unique_products = sorted(set(products))   # sorted → canonical order, set → no dupes
            if len(unique_products) > 1:
                for i in range(len(unique_products)):
                    for j in range(i + 1, len(unique_products)):
                        product_pairs.append((unique_products[i], unique_products[j]))

        if not product_pairs:
            return pd.DataFrame()

        pair_counts = pd.DataFrame(product_pairs, columns=["Product A", "Product B"])
        pair_frequency = (
            pair_counts.groupby(["Product A", "Product B"])
            .size()
            .reset_index(name="Times Bought Together")
        )

        return pair_frequency.sort_values("Times Bought Together", ascending=False).head(20)

    except Exception as e:
        logger.error(f"Error finding bundling opportunities: {str(e)}")
        return pd.DataFrame()


def payment_terms_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze sales by payment terms."""
    if df.empty or "payment_terms" not in df.columns:
        return pd.DataFrame()

    try:
        df_filtered = df[df["payment_terms"].notna()].copy()
        if df_filtered.empty:
            return pd.DataFrame()

        payment_analysis = df_filtered.groupby("payment_terms").agg(
            Total_Revenue       =("revenue",       "sum"),
            Avg_Transaction     =("revenue",       "mean"),
            Num_Transactions    =("revenue",       "count"),
            Unique_Customers    =("customer_name", "nunique"),
        ).reset_index()

        payment_analysis.columns = [
            "Payment Terms", "Total Revenue", "Avg Transaction",
            "Number of Transactions", "Unique Customers",
        ]

        total_revenue = payment_analysis["Total Revenue"].sum()
        payment_analysis["% of Total Revenue"] = (
            payment_analysis["Total Revenue"] / total_revenue * 100
        ).round(2)

        return payment_analysis.sort_values("Total Revenue", ascending=False)

    except Exception as e:
        logger.error(f"Error analyzing payment terms: {str(e)}")
        return pd.DataFrame()