import streamlit as st
from pymongo import MongoClient
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import datetime
import plotly.graph_objects as go
import io

# Theme toggle (manual)
theme = st.sidebar.radio("🌗 Theme", ["Light", "Dark"])
dark_mode = theme == "Dark"

# Page config
st.set_page_config(page_title="BTC Metrics Dashboard", layout="wide")
st.title("📈 Bitcoin (BTC) Metrics Dashboard")

# CSS styling with hover, icons, and theme-aware support
bg_color = "#2c2f33" if dark_mode else "#f8f9fa"
text_color = "#f1f1f1" if dark_mode else "#333"
label_color = "#ccc" if dark_mode else "#666"

st.markdown(f"""
<style>
.card {{
    background-color: {bg_color};
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    text-align: center;
    transition: all 0.3s ease-in-out;
}}
.card:hover {{
    transform: scale(1.03);
    box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}}
.card .value {{
    font-size: 1.8rem;
    font-weight: bold;
    color: {text_color};
}}
.card .label {{
    font-size: 1rem;
    color: {label_color};
}}
</style>
""", unsafe_allow_html=True)

# Auto-refresh every 10 seconds
st_autorefresh(interval=10000, limit=None, key="btc-refresh")

# MongoDB client (cached)
@st.cache_resource
def get_mongo_client():
    return MongoClient("mongodb://mongodb:27017/")

# Fetch data (cached 60s)
@st.cache_data(ttl=60)
def get_data():
    client = get_mongo_client()
    db = client["btc_db"]
    collection = db["metrics"]
    data = list(collection.find().sort("timestamp", -1).limit(100))
    df = pd.DataFrame(data)
    if '_id' in df.columns:
        df.drop(columns=['_id'], inplace=True)
    return df

# Format large numbers helper
def format_large_number(n):
    try:
        n = float(n)
        if n >= 1_000_000_000:
            return f"${n/1_000_000_000:.2f}B"
        elif n >= 1_000_000:
            return f"${n/1_000_000:.2f}M"
        elif n >= 1_000:
            return f"${n/1_000:.2f}K"
        else:
            return f"${n:.2f}"
    except:
        return str(n)

# Clean dataframe for Excel export (convert lists/dicts to strings)
def clean_for_excel(df):
    df_clean = df.copy()
    for col in df_clean.columns:
        if df_clean[col].apply(lambda x: isinstance(x, (list, dict))).any():
            df_clean[col] = df_clean[col].astype(str)
    return df_clean

# Remove timezone info from datetime columns for Excel export
def remove_timezone(df):
    df_copy = df.copy()
    for col in df_copy.select_dtypes(include=['datetimetz']).columns:
        df_copy[col] = df_copy[col].dt.tz_localize(None)
    return df_copy

# Load data with spinner
with st.spinner("Loading BTC metrics..."):
    df = get_data()

# Show last update time
st.write("🕒 Last update:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if not df.empty:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values('timestamp', inplace=True)
    latest = df.iloc[-1]

    price_usd = latest.get('price_usd', 0)
    price_change_24h = latest.get('price_change_24h', 0)
    volume_24h = latest.get('volume_24h', 0)
    market_cap = latest.get('market_cap', 0)

    # Threshold alert
    if price_usd < 25000:
        st.error("🔔 Alert: BTC Price dropped below $25,000!")

    # KPI cards with icons in 4 columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="value">💰 {format_large_number(price_usd)}</div>
            <div class="label">BTC Price (USD)</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        sign = "+" if price_change_24h > 0 else ""
        color = "green" if price_change_24h > 0 else "red"
        st.markdown(f"""
        <div class="card">
            <div class="value" style="color:{color};">📉 {sign}{price_change_24h:.2f}%</div>
            <div class="label">24h Change</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="value">🔄 {format_large_number(volume_24h)}</div>
            <div class="label">24h Volume</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="card">
            <div class="value">🏦 {format_large_number(market_cap)}</div>
            <div class="label">Market Cap</div>
        </div>
        """, unsafe_allow_html=True)

    # Plot BTC price chart (autoscale)
    df_tail = df.tail(100)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_tail['timestamp'],
        y=df_tail['price_usd'],
        mode='lines+markers',
        name='BTC Price',
        line=dict(color='royalblue', width=2)
    ))
    fig.update_layout(
        title="📊 BTC Price Over Time (USD)",
        height=420,
        margin=dict(l=20, r=20, t=50, b=30),
        xaxis=dict(showticklabels=False),
        yaxis=dict(
            title="USD",
            showgrid=True,
            tickformat=".0f",
            autorange=True
        ),
        showlegend=False,
        autosize=True,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Export buttons side by side
    st.markdown("### 📤 Export Data")
    col_csv, col_excel = st.columns(2)

    with col_csv:
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="btc_metrics.csv",
            mime="text/csv"
        )

    with col_excel:
        excel_buffer = io.BytesIO()
        df_clean = clean_for_excel(df)
        df_clean = remove_timezone(df_clean)  # Remove timezone info here
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df_clean.to_excel(writer, index=False)
        st.download_button(
            label="Download Excel",
            data=excel_buffer.getvalue(),
            file_name="btc_metrics.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.warning("⚠️ No data available to display.")
