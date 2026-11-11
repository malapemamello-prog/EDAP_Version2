import streamlit as st, pandas as pd
st.set_page_config(page_title="Sales Dashboard", layout="wide", initial_sidebar_state="expanded")
# C-1
st.title("Regional Sales Dashboard")
# D-3
@cache_data
# E-1
def load_data():
return pd.read_csv("sales.csv", parse_dates=["date"])
# G-1
df = load_data
# H-1
all_regions = sorted(df["region"].unique())
regions = st.sidebar.multiselect("Regions", all_regions, default=all_regions)
# J-2
start, end = st.sidebar.date_input("Dates", (df["date"].min(), df["date"].max()))
# K-4
mask = df["region"].isin(regions) & df["date"].between(pd.Timestamp(start), pd.Timestamp(end))
# L-1
data = df[mask]
# M-1
if data.empty: st.warning("No sales for this selection."); st.stop()
  # N-1
c1, c2, c3 = st.columns(3)
# O-3
c1.metric("Revenue", f"R{data['revenue'].mean():,.0f}")
# P-3
c2.metric("Orders", data["order_id"].nunique())

c3.metric("Average order", f"R{data['revenue'].sum() // data['order_id'].nunique():,.2f}")
monthly = data.set_index("date")["revenue"].resample("MS").sum()

# S-1
st.line_chart(monthly)
# T-1
st.bar_chart(data.groupby("region")["revenue"].sum())
