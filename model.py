import pandas as pd
import xgboost as xgb
import numpy as np



def forecast(df):

    daily = (
        df.groupby("invoice_date")["revenue"]
        .sum()
        .reset_index()
    )

    if len(daily) < 5:
        return pd.DataFrame()

    daily["day"] = (
        daily["invoice_date"] - daily["invoice_date"].min()
    ).dt.days

    daily["dow"] = daily["invoice_date"].dt.dayofweek

    daily["month"] = daily["invoice_date"].dt.month

    daily["lag1"] = daily["revenue"].shift(1)

    daily["rolling_mean"] = (
        daily["revenue"]
        .rolling(3)
        .mean()
    )

    daily = daily.dropna()

    X = daily[[
        "day",
        "dow",
        "month",
        "lag1",
        "rolling_mean"
    ]]

    y = daily["revenue"]

    model = xgb.XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5
    )

    model.fit(X, y)

    future = []

    last_day = daily["day"].max()
    last_revenue = daily["revenue"].iloc[-1]
    rolling = daily["rolling_mean"].iloc[-1]

    for i in range(1, 8):

        future.append([
            last_day + i,
            (last_day + i) % 7,
            daily["month"].iloc[-1],
            last_revenue,
            rolling
        ])

    future = pd.DataFrame(
        future,
        columns=[
            "day",
            "dow",
            "month",
            "lag1",
            "rolling_mean"
        ]
    )

    preds = model.predict(future)

    return pd.DataFrame({
        "Day": [f"Day {i}" for i in range(1, 8)],
        "Predicted Revenue": preds.round(2)
    })