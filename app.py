# import streamlit as st
# import yfinance as yf
# import pandas as pd
# import plotly.graph_objects as go
# import technical_indicators as ti  # your custom indicators module
# from utils import compute_final

# # ------------------------------
# # Page config + styling
# # ------------------------------
# st.set_page_config(page_title="StockPulse — Stock Predictor", layout="wide")

# st.markdown(
#     """
# <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:6px;padding:10px;">
#     <div style="font-size:46px;font-weight:800;letter-spacing:1px">StockPulse</div>
# </div>
# """,
#     unsafe_allow_html=True,
# )

# st.markdown(
#     """
# <style>
#   .stApp { background: linear-gradient(180deg, #071024 0%, #031923 100%); }
#   .stBlock > div { color: #e6eef8; }
#   .metric-box { padding: 12px 16px; border-radius: 8px; background: rgba(255,255,255,0.03); }
#   .prediction { font-size:20px; font-weight:700; }
#   .signal-buy { color: #16a34a; }
#   .signal-wait { color: #f97316; }
#   .card { background: rgba(255,255,255,0.02); border-radius: 8px; padding: 12px; }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # ------------------------------
# # Helper: load data
# # ------------------------------
# def load_data(ticker: str) -> pd.DataFrame:
#     df = yf.download(ticker, period="1y", interval="1d")
#     if df.empty:
#         return pd.DataFrame()
#     # handle yfinance multi-index columns in some versions
#     df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
#     df = df.reset_index()  # Date becomes a column
#     return df

# # ------------------------------
# # Sidebar controls
# # ------------------------------
# with st.sidebar:
#     st.header("Controls")
#     ticker = st.text_input("Ticker (e.g. AAPL, TSLA, INFY.BO, RELIANCE.NS)", "AAPL")
#     horizon = st.slider("Prediction horizon (days)", 1, 30, 5)
#     indicator_options = [
#         "MACD",
#         "RSI",
#         "Momentum",
#         "Bollinger Bands",
#         "ATR",
#         "OBV",
#         "Pivot Points (PPSR)",
#         "Stochastic Oscillator",
#         "TRIX",
#         "ADX",
#         "Mass Index",
#         "KST Oscillator",
#         "TRSI",  # keep as placeholder if you have this
#         "TSI",
#         "Accumulation/Distribution",
#         "Chaikin Oscillator",
#         "Money Flow Index (MFI)",
#         "On Balance Volume (OBV)",
#         "Force Index",
#         "CCI",
#         "Coppock Curve",
#         "Keltner Channel",
#         "Ultimate Oscillator",
#         "Donchian Channel",
#         "Standard Deviation",
#         "Ease of Movement (EoM)",
#     ]
#     selected_indicators = st.multiselect("Select indicators", indicator_options, default=["MACD"])
#     run = st.button("Run Analysis")

# # ------------------------------
# # Main app logic
# # ------------------------------
# if run:
#     df = load_data(ticker)
#     if df.empty:
#         st.error("No data found for this ticker — try a different symbol.")
#     else:
#         # prediction (safe fallback on error)
#         try:
#             prob = float(compute_final(ticker, horizon))
#         except Exception as e:
#             st.warning(f"Prediction failed, defaulting probability to 0.0 ({e})")
#             prob = 0.0

#         signal = "BUY ✅" if prob >= 0.6 else "WAIT ⏳"
#         badge_class = "signal-buy" if prob >= 0.6 else "signal-wait"

#         # layout: left (metrics), right (charts)
#         left, right = st.columns([1, 3])
#         with left:
#             st.markdown(
#                 f"""
#                 <div class="metric-box">
#                   <div class="prediction {badge_class}">{signal}</div>
#                   <div style="opacity:0.9">Probability: {prob:.2f}</div>
#                   <div style="margin-top:8px;font-size:12px;opacity:0.8">Horizon: {horizon} days</div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )

#         with right:
#             st.write(f"### {ticker} — Last 1 Year")

#             # Candlestick figure
#             fig = go.Figure(
#                 data=[
#                     go.Candlestick(
#                         x=df["Date"],
#                         open=df["Open"],
#                         high=df["High"],
#                         low=df["Low"],
#                         close=df["Close"],
#                         name="Price",
#                     )
#                 ]
#             )
#             fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=500)
#             st.plotly_chart(fig, use_container_width=True)

#         # ------------------------------
#         # Indicators: process each selection
#         # ------------------------------
#         for indicator in selected_indicators:
#             st.markdown(f"### {indicator}")
#             try:
#                 # MACD example: ti.macd returns a dataframe with columns MACD_12_26, MACDsign_12_26, MACDdiff_12_26
#                 if indicator == "MACD":
#                     dfi = ti.macd(df.copy(), 12, 26)
#                     fig_ind = go.Figure()
#                     fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["MACD_12_26"], name="MACD"))
#                     fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["MACDsign_12_26"], name="Signal"))
#                     fig_ind.add_trace(go.Bar(x=dfi["Date"], y=dfi["MACDdiff_12_26"], name="MACD diff"))
#                     fig_ind.update_layout(template="plotly_dark", height=350)
#                     st.plotly_chart(fig_ind, use_container_width=True)

#                 elif indicator == "RSI":
#                     dfi = ti.relative_strength_index(df.copy(), 14)
#                     # ensure RSI column exists
#                     rsi_col = [c for c in dfi.columns if c.lower().startswith("rsi")]
#                     if rsi_col:
#                         st.line_chart(dfi.set_index("Date")[rsi_col[0]])
#                     else:
#                         st.write("RSI calculation did not return expected column.")

#                 elif indicator == "Momentum":
#                     dfi = ti.momentum(df.copy(), 10)
#                     mom_col = [c for c in dfi.columns if "momentum" in c.lower() or "moment" in c.lower()]
#                     if mom_col:
#                         st.line_chart(dfi.set_index("Date")[mom_col[0]])
#                     else:
#                         st.write("Momentum function did not return expected column.")

#                 elif indicator == "Bollinger Bands":
#                     dfi = ti.bollinger_bands(df.copy(), 20)
#                     fig_ind = go.Figure()
#                     fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["BB_Middle"], name="Middle"))
#                     fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["BB_Upper"], name="Upper"))
#                     fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["BB_Lower"], name="Lower"))
#                     fig_ind.update_layout(template="plotly_dark", height=350)
#                     st.plotly_chart(fig_ind, use_container_width=True)

#                 elif indicator == "ATR":
#                     dfi = ti.average_true_range(df.copy(), 14)
#                     atr_col = [c for c in dfi.columns if "atr" in c.lower()]
#                     if atr_col:
#                         st.line_chart(dfi.set_index("Date")[atr_col[0]])
#                     else:
#                         st.write("ATR did not return expected column.")

#                 elif indicator == "OBV" or indicator == "On Balance Volume (OBV)":
#                     dfi = ti.on_balance_volume(df.copy(), horizon)
#                     obv_col = [c for c in dfi.columns if "obv" in c.lower()]
#                     if obv_col:
#                         st.line_chart(dfi.set_index("Date")[obv_col[0]])
#                     else:
#                         # fallback to computing simple OBV if function missing
#                         st.write("OBV function didn't return expected column. Plotting Close price as fallback.")
#                         st.line_chart(df.set_index("Date")["Close"])

#                 elif indicator == "Pivot Points (PPSR)":
#                     dfi = ti.ppsr(df.copy())
#                     fig_ind = go.Figure()
#                     for name in ["PP", "S1", "R1", "S2", "R2", "S3", "R3"]:
#                         if name in dfi.columns:
#                             fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[name], mode="lines", name=name))
#                     fig_ind.update_layout(template="plotly_dark", height=350)
#                     st.plotly_chart(fig_ind, use_container_width=True)

#                 elif indicator == "Stochastic Oscillator":
#                     dfi = ti.stochastic_oscillator_d(df.copy(), horizon)
#                     k_col = next((c for c in dfi.columns if "%K" in c or "so%k" in c.lower()), None)
#                     d_col = next((c for c in dfi.columns if "%D" in c or "so%d" in c.lower()), None)
#                     fig_ind = go.Figure()
#                     if k_col:
#                         fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[k_col], name="%K"))
#                     if d_col:
#                         fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[d_col], name="%D"))
#                     fig_ind.update_layout(template="plotly_dark", height=350)
#                     st.plotly_chart(fig_ind, use_container_width=True)

#                 elif indicator == "TRIX":
#                     dfi = ti.trix(df.copy(), horizon)
#                     trix_col = next((c for c in dfi.columns if "trix" in c.lower()), None)
#                     if trix_col:
#                         st.line_chart(dfi.set_index("Date")[trix_col])
#                     else:
#                         st.write("TRIX column not found.")

#                 elif indicator == "ADX":
#                     dfi = ti.average_directional_movement_index(df.copy(), 14)
#                     adx_col = [c for c in dfi.columns if "adx" in c.lower()]
#                     if adx_col:
#                         st.line_chart(dfi.set_index("Date")[adx_col[0]])
#                     else:
#                         st.write("ADX column not found.")

#                 elif indicator == "Mass Index":
#                     dfi = ti.mass_index(df.copy())
#                     mi_col = next((c for c in dfi.columns if "mass" in c.lower() or "mass index" in c.lower()), None)
#                     if mi_col:
#                         st.line_chart(dfi.set_index("Date")[mi_col])
#                     else:
#                         st.write("Mass Index column not found.")

#                 elif indicator == "KST Oscillator":
#                     # example parameters (you can expose these in sidebar if needed)
#                     r1, r2, r3, r4 = 10, 15, 20, 30
#                     n1, n2, n3, n4 = 10, 10, 10, 15
#                     dfi = ti.kst_oscillator(df.copy(), r1, r2, r3, r4, n1, n2, n3, n4)
#                     kst_col = [c for c in dfi.columns if "kst" in c.lower() and "signal" not in c.lower()]
#                     kst_signal_col = [c for c in dfi.columns if "kst" in c.lower() and "signal" in c.lower()]
#                     fig_ind = go.Figure()
#                     if kst_col:
#                         fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[kst_col[0]], name="KST"))
#                     if kst_signal_col:
#                         fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[kst_signal_col[0]], name="KST Signal"))
#                     fig_ind.update_layout(template="plotly_dark", height=350)
#                     st.plotly_chart(fig_ind, use_container_width=True)

#                 elif indicator in ("TSI", "True Strength Index (TSI)"):
#                     dfi = ti.true_strength_index(df.copy(), 25, 13)
#                     tsi_col = next((c for c in dfi.columns if "tsi" in c.lower()), None)
#                     if tsi_col:
#                         st.line_chart(dfi.set_index("Date")[tsi_col])
#                     else:
#                         st.write("TSI column not found.")

#                 elif indicator == "Accumulation/Distribution":
#                     dfi = ti.accumulation_distribution(df.copy(), horizon)
#                     acc_col = next((c for c in dfi.columns if "acc" in c.lower() or "acc/dist" in c.lower()), None)
#                     if acc_col:
#                         st.line_chart(dfi.set_index("Date")[acc_col])
#                     else:
#                         st.write("Accumulation/Distribution column not found.")

#                 elif indicator == "Chaikin Oscillator":
#                     dfi = ti.chaikin_oscillator(df.copy())
#                     chaikin_col = next((c for c in dfi.columns if "chaikin" in c.lower()), None)
#                     if chaikin_col:
#                         st.line_chart(dfi.set_index("Date")[chaikin_col])
#                     else:
#                         st.write("Chaikin column not found.")

#                 elif indicator == "Money Flow Index (MFI)":
#                     dfi = ti.money_flow_index(df.copy(), horizon)
#                     mfi_col = next((c for c in dfi.columns if "mfi" in c.lower()), None)
#                     if mfi_col:
#                         st.line_chart(dfi.set_index("Date")[mfi_col])
#                     else:
#                         st.write("MFI column not found.")

#                 elif indicator == "Force Index":
#                     dfi = ti.force_index(df.copy(), horizon)
#                     f_col = next((c for c in dfi.columns if "force" in c.lower()), None)
#                     if f_col:
#                         st.line_chart(dfi.set_index("Date")[f_col])
#                     else:
#                         st.write("Force Index column not found.")

#                 elif indicator == "CCI" or indicator == "Commodity Channel Index (CCI)":
#                     dfi = ti.commodity_channel_index(df.copy(), 20)
#                     cci_col = next((c for c in dfi.columns if "cci" in c.lower()), None)
#                     if cci_col:
#                         st.line_chart(dfi.set_index("Date")[cci_col])
#                     else:
#                         st.write("CCI column not found.")

#                 elif indicator == "Coppock Curve":
#                     dfi = ti.coppock_curve(df.copy(), horizon)
#                     copp_col = next((c for c in dfi.columns if "copp" in c.lower()), None)
#                     if copp_col:
#                         st.line_chart(dfi.set_index("Date")[copp_col])
#                     else:
#                         st.write("Coppock column not found.")

#                 elif indicator == "Keltner Channel":
#                     dfi = ti.keltner_channel(df.copy(), horizon)
#                     keys = [k for k in dfi.columns if "kelch" in k.lower() or "kelt" in k.lower()]
#                     fig_ind = go.Figure()
#                     for key in keys:
#                         fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[key], name=key))
#                     fig_ind.update_layout(template="plotly_dark", height=350)
#                     st.plotly_chart(fig_ind, use_container_width=True)

#                 elif indicator == "Ultimate Oscillator":
#                     dfi = ti.ultimate_oscillator(df.copy())
#                     u_col = next((c for c in dfi.columns if "ultimate" in c.lower() or "ultimate_osc" in c.lower()), None)
#                     if u_col:
#                         st.line_chart(dfi.set_index("Date")[u_col])
#                     else:
#                         st.write("Ultimate Oscillator column not found.")

#                 elif indicator == "Donchian Channel":
#                     dfi = ti.donchian_channel(df.copy(), horizon)
#                     don_col = next((c for c in dfi.columns if "donchian" in c.lower()), None)
#                     if don_col:
#                         st.line_chart(dfi.set_index("Date")[don_col])
#                     else:
#                         st.write("Donchian column not found.")

#                 elif indicator == "Standard Deviation":
#                     dfi = ti.standard_deviation(df.copy(), horizon)
#                     std_col = next((c for c in dfi.columns if "std" in c.lower()), None)
#                     if std_col:
#                         st.line_chart(dfi.set_index("Date")[std_col])
#                     else:
#                         st.write("Standard Deviation column not found.")

#                 elif indicator == "Ease of Movement (EoM)":
#                     dfi = ti.ease_of_movement(df.copy(), horizon)
#                     eom_col = next((c for c in dfi.columns if "eom" in c.lower() or "ease" in c.lower()), None)
#                     if eom_col:
#                         st.line_chart(dfi.set_index("Date")[eom_col])
#                     else:
#                         st.write("Ease of Movement column not found.")

#                 else:
#                     # fallback if an indicator is selected but not implemented
#                     st.write(f"{indicator} is not implemented in the app or the TI module. Showing Close price instead.")
#                     st.line_chart(df.set_index("Date")["Close"])

#             except Exception as exc:
#                 st.write(f"Indicator plotting failed for {indicator}: {exc}")



import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import technical_indicators as ti
from utils import compute_final

# ------------------------------
# Page config + Premium styling
# ------------------------------
st.set_page_config(
    page_title="StockPulse — AI Stock Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject premium CSS with gradient backgrounds, glass morphism, and animations
st.markdown(
    """
<style>
    /* Main app background with deep gradient */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 25%, #0f1729 50%, #1e2139 75%, #0a0e27 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f3a 0%, #0f1729 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.1);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e7ff;
    }
    
    /* Header styling */
    [data-testid="stSidebar"] h2 {
        color: #818cf8;
        font-weight: 700;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(129, 140, 248, 0.3);
        margin-bottom: 20px;
    }
    
    /* Input fields */
    .stTextInput input {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(129, 140, 248, 0.3);
        border-radius: 8px;
        color: #e0e7ff;
        padding: 10px;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus {
        border-color: #818cf8;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2);
        background: rgba(99, 102, 241, 0.15);
    }
    
    /* Slider styling */
    .stSlider {
        padding: 10px 0;
    }
    
    /* Multiselect */
    .stMultiSelect [data-baseweb="select"] {
        background: rgba(99, 102, 241, 0.1);
        border-radius: 8px;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 16px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.6);
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
    }
    
    /* Glass morphism card */
    .glass-card {
        background: rgba(30, 33, 57, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(129, 140, 248, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.3);
        border-color: rgba(129, 140, 248, 0.4);
    }
    
    /* Metric box with glow effect */
    .metric-box {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        border-radius: 16px;
        padding: 28px;
        border: 2px solid rgba(129, 140, 248, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(129, 140, 248, 0.1) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .metric-box:hover {
        transform: scale(1.02);
        border-color: rgba(129, 140, 248, 0.5);
        box-shadow: 0 12px 48px rgba(99, 102, 241, 0.4);
    }
    
    /* Prediction styling */
    .prediction {
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }
    
    .signal-buy {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow-green 2s ease-in-out infinite;
    }
    
    .signal-wait {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow-orange 2s ease-in-out infinite;
    }
    
    @keyframes glow-green {
        0%, 100% { filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.6)); }
        50% { filter: drop-shadow(0 0 16px rgba(16, 185, 129, 0.9)); }
    }
    
    @keyframes glow-orange {
        0%, 100% { filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.6)); }
        50% { filter: drop-shadow(0 0 16px rgba(245, 158, 11, 0.9)); }
    }
    
    .probability-text {
        font-size: 18px;
        color: #c7d2fe;
        font-weight: 600;
        margin-bottom: 4px;
        position: relative;
        z-index: 1;
    }
    
    .horizon-text {
        font-size: 14px;
        color: #a5b4fc;
        font-weight: 500;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid rgba(129, 140, 248, 0.2);
        position: relative;
        z-index: 1;
    }
    
    /* Section headers */
    h3 {
        color: #e0e7ff;
        font-weight: 700;
        font-size: 24px;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(129, 140, 248, 0.3);
        background: linear-gradient(90deg, #818cf8 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Chart containers */
    .stPlotlyChart {
        background: rgba(30, 33, 57, 0.5);
        border-radius: 12px;
        padding: 12px;
        border: 1px solid rgba(129, 140, 248, 0.15);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Line chart styling */
    .stLineChart {
        background: rgba(30, 33, 57, 0.5);
        border-radius: 12px;
        padding: 12px;
        border: 1px solid rgba(129, 140, 248, 0.15);
    }
    
    /* Error and warning messages */
    .stAlert {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
        color: #fca5a5;
    }
    
    /* Text color */
    .stMarkdown, p, span, div {
        color: #e0e7ff;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 33, 57, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(129, 140, 248, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(129, 140, 248, 0.7);
    }
</style>
""",
    unsafe_allow_html=True,
)

# Premium header with animated gradient
st.markdown(
    """
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px 10px 30px 10px;">
    <div style="font-size:56px;font-weight:900;letter-spacing:3px;background:linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #c084fc 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:8px;text-shadow:0 4px 20px rgba(129,140,248,0.5);">
        StockPulse
    </div>
    <div style="font-size:16px;color:#a5b4fc;font-weight:500;letter-spacing:4px;text-transform:uppercase;">
        AI-Powered Stock Predictor
    </div>
    <div style="width:80px;height:3px;background:linear-gradient(90deg, transparent, #818cf8, transparent);margin-top:12px;border-radius:2px;"></div>
</div>
""",
    unsafe_allow_html=True,
)

# ------------------------------
# Helper: load data
# ------------------------------
def load_data(ticker: str) -> pd.DataFrame:
    df = yf.download(ticker, period="1y", interval="1d")
    if df.empty:
        return pd.DataFrame()
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df = df.reset_index()
    return df

# ------------------------------
# Sidebar controls with premium styling
# ------------------------------
with st.sidebar:
    st.markdown("## 🎯 Analysis Controls")
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    
    ticker = st.text_input("📊 Stock Ticker", "AAPL", help="Enter ticker symbol (e.g., AAPL, TSLA, INFY.BO, RELIANCE.NS)")
    
    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    
    horizon = st.slider("📅 Prediction Horizon (days)", 1, 30, 5, help="Number of days to predict ahead")
    
    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    
    indicator_options = [
        "MACD",
        "RSI",
        "Momentum",
        "Bollinger Bands",
        "ATR",
        "OBV",
        "Pivot Points (PPSR)",
        "Stochastic Oscillator",
        "TRIX",
        "ADX",
        "Mass Index",
        "KST Oscillator",
        "TSI",
        "Accumulation/Distribution",
        "Chaikin Oscillator",
        "Money Flow Index (MFI)",
        "On Balance Volume (OBV)",
        "Force Index",
        "CCI",
        "Coppock Curve",
        "Keltner Channel",
        "Ultimate Oscillator",
        "Donchian Channel",
        "Standard Deviation",
        "Ease of Movement (EoM)",
    ]
    
    selected_indicators = st.multiselect(
        "📈 Technical Indicators",
        indicator_options,
        default=["MACD"],
        help="Select indicators to display"
    )
    
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    run = st.button("🚀 Run Analysis")
    
    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align:center;padding:15px;font-size:12px;color:#a5b4fc;'>
            <p style='margin:0;'>Powered by AI & Machine Learning</p>
            <p style='margin:5px 0 0 0;opacity:0.7;'>© 2024 StockPulse</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------------
# Main app logic
# ------------------------------
if run:
    df = load_data(ticker)
    if df.empty:
        st.error("❌ No data found for this ticker — please try a different symbol.")
    else:
        # Prediction calculation
        try:
            prob = float(compute_final(ticker, horizon))
        except Exception as e:
            st.warning(f"⚠️ Prediction failed, using default probability ({e})")
            prob = 0.0

        signal = "BUY ✅" if prob >= 0.6 else "WAIT ⏳"
        badge_class = "signal-buy" if prob >= 0.6 else "signal-wait"

        # Layout: left (metrics), right (charts)
        left, right = st.columns([1, 3], gap="large")
        
        with left:
            st.markdown(
                f"""
                <div class="metric-box">
                  <div class="prediction {badge_class}">{signal}</div>
                  <div class="probability-text">Confidence: {prob:.1%}</div>
                  <div class="horizon-text">📅 Forecast: {horizon} day{'s' if horizon > 1 else ''}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
            
            # Additional info card
            latest_close = df["Close"].iloc[-1]
            prev_close = df["Close"].iloc[-2] if len(df) > 1 else latest_close
            change = latest_close - prev_close
            change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
            change_color = "#10b981" if change >= 0 else "#ef4444"
            
            st.markdown(
                f"""
                <div class="glass-card">
                    <div style="font-size:14px;color:#a5b4fc;margin-bottom:8px;font-weight:600;">LATEST PRICE</div>
                    <div style="font-size:28px;font-weight:800;color:#e0e7ff;margin-bottom:4px;">${latest_close:.2f}</div>
                    <div style="font-size:14px;color:{change_color};font-weight:600;">
                        {'▲' if change >= 0 else '▼'} ${abs(change):.2f} ({abs(change_pct):.2f}%)
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with right:
            st.markdown(f"### 📊 {ticker} — Price Chart (1 Year)")

            # Premium candlestick chart
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=df["Date"],
                        open=df["Open"],
                        high=df["High"],
                        low=df["Low"],
                        close=df["Close"],
                        name="Price",
                        increasing_line_color='#10b981',
                        decreasing_line_color='#ef4444',
                        increasing_fillcolor='rgba(16, 185, 129, 0.3)',
                        decreasing_fillcolor='rgba(239, 68, 68, 0.3)'
                    )
                ]
            )
            
            fig.update_layout(
                template="plotly_dark",
                xaxis_rangeslider_visible=False,
                height=500,
                paper_bgcolor='rgba(30, 33, 57, 0.5)',
                plot_bgcolor='rgba(30, 33, 57, 0.3)',
                font=dict(color='#e0e7ff'),
                xaxis=dict(
                    gridcolor='rgba(129, 140, 248, 0.1)',
                    showgrid=True
                ),
                yaxis=dict(
                    gridcolor='rgba(129, 140, 248, 0.1)',
                    showgrid=True
                ),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            
            st.plotly_chart(fig, use_container_width=True)

        # ------------------------------
        # Technical Indicators Section
        # ------------------------------
        if selected_indicators:
            st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
            st.markdown("## 📈 Technical Indicators Analysis")
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        for indicator in selected_indicators:
            st.markdown(f"### 🔍 {indicator}")
            try:
                if indicator == "MACD":
                    dfi = ti.macd(df.copy(), 12, 26)
                    fig_ind = go.Figure()
                    fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["MACD_12_26"], name="MACD", line=dict(color='#818cf8', width=2)))
                    fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["MACDsign_12_26"], name="Signal", line=dict(color='#f59e0b', width=2)))
                    fig_ind.add_trace(go.Bar(x=dfi["Date"], y=dfi["MACDdiff_12_26"], name="Histogram", marker_color='rgba(139, 92, 246, 0.5)'))
                    fig_ind.update_layout(
                        template="plotly_dark",
                        height=350,
                        paper_bgcolor='rgba(30, 33, 57, 0.5)',
                        plot_bgcolor='rgba(30, 33, 57, 0.3)',
                        font=dict(color='#e0e7ff'),
                        xaxis=dict(gridcolor='rgba(129, 140, 248, 0.1)'),
                        yaxis=dict(gridcolor='rgba(129, 140, 248, 0.1)'),
                        margin=dict(l=10, r=10, t=10, b=10)
                    )
                    st.plotly_chart(fig_ind, use_container_width=True)

                elif indicator == "RSI":
                    dfi = ti.relative_strength_index(df.copy(), 14)
                    rsi_col = [c for c in dfi.columns if c.lower().startswith("rsi")]
                    if rsi_col:
                        st.line_chart(dfi.set_index("Date")[rsi_col[0]], color='#818cf8')
                    else:
                        st.write("RSI calculation did not return expected column.")

                elif indicator == "Momentum":
                    dfi = ti.momentum(df.copy(), 10)
                    mom_col = [c for c in dfi.columns if "momentum" in c.lower() or "moment" in c.lower()]
                    if mom_col:
                        st.line_chart(dfi.set_index("Date")[mom_col[0]], color='#a78bfa')
                    else:
                        st.write("Momentum function did not return expected column.")

                elif indicator == "Bollinger Bands":
                    dfi = ti.bollinger_bands(df.copy(), 20)
                    fig_ind = go.Figure()
                    fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["BB_Middle"], name="Middle", line=dict(color='#818cf8', width=2)))
                    fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["BB_Upper"], name="Upper", line=dict(color='#10b981', width=1.5)))
                    fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["BB_Lower"], name="Lower", line=dict(color='#ef4444', width=1.5)))
                    fig_ind.update_layout(
                        template="plotly_dark",
                        height=350,
                        paper_bgcolor='rgba(30, 33, 57, 0.5)',
                        plot_bgcolor='rgba(30, 33, 57, 0.3)',
                        font=dict(color='#e0e7ff'),
                        xaxis=dict(gridcolor='rgba(129, 140, 248, 0.1)'),
                        yaxis=dict(gridcolor='rgba(129, 140, 248, 0.1)'),
                        margin=dict(l=10, r=10, t=10, b=10)
                    )
                    st.plotly_chart(fig_ind, use_container_width=True)

                elif indicator == "ATR":
                    dfi = ti.average_true_range(df.copy(), 14)
                    atr_col = [c for c in dfi.columns if "atr" in c.lower()]
                    if atr_col:
                        st.line_chart(dfi.set_index("Date")[atr_col[0]], color='#f59e0b')
                    else:
                        st.write("ATR did not return expected column.")

                elif indicator == "OBV" or indicator == "On Balance Volume (OBV)":
                    dfi = ti.on_balance_volume(df.copy(), horizon)
                    obv_col = [c for c in dfi.columns if "obv" in c.lower()]
                    if obv_col:
                        st.line_chart(dfi.set_index("Date")[obv_col[0]], color='#8b5cf6')
                    else:
                        st.write("OBV function didn't return expected column.")

                elif indicator == "Pivot Points (PPSR)":
                    dfi = ti.ppsr(df.copy())
                    fig_ind = go.Figure()
                    colors = {'PP': '#818cf8', 'S1': '#ef4444', 'R1': '#10b981', 'S2': '#dc2626', 'R2': '#059669', 'S3': '#b91c1c', 'R3': '#047857'}
                    for name in ["PP", "S1", "R1", "S2", "R2", "S3", "R3"]:
                        if name in dfi.columns:
                            fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[name], mode="lines", name=name, line=dict(color=colors.get(name, '#818cf8'), width=1.5)))
                    fig_ind.update_layout(
                        template="plotly_dark",
                        height=350,
                        paper_bgcolor='rgba(30, 33, 57, 0.5)',
                        plot_bgcolor='rgba(30, 33, 57, 0.3)',
                        font=dict(color='#e0e7ff'),
                        xaxis=dict(gridcolor='rgba(129, 140, 248, 0.1)'),
                        yaxis=dict(gridcolor='rgba(129, 140, 248, 0.1)'),
                        margin=dict(l=10, r=10, t=10, b=10)
                    )
                    st.plotly_chart(fig_ind, use_container_width=True)

                elif indicator == "Stochastic Oscillator":
                    dfi = ti.stochastic_oscillator_d(df.copy(), horizon)
                    k_col = next((c for c in dfi.columns if "%K" in c or "so%k" in c.lower()), None)
                    d_col = next((c for c in dfi.columns if "%D" in c or "so%d" in c.lower()), None)
                    fig_ind = go.Figure()
                    if k_col:
                        fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[k_col], name="%K", line=dict(color='#818cf8', width=2)))
                    if d_col:
                        fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[d_col], name="%D", line=dict(color='#f59e0b', width=2)))
                    fig_ind.update_layout(
                        template="plotly_dark",
                        height=350,
                        paper_bgcolor='rgba(30, 33, 57, 0.5)',
                        plot_bgcolor='rgba(30, 33, 57, 0.3)',
                        font=dict(color='#e0e7ff'),
                        xaxis=dict(gridcolor='rgba(129, 140, 248, 0.1)'),
                        yaxis=dict(gridcolor='rgba(129, 140, 248, 0.1)'),
                        margin=dict(l=10, r=10, t=10, b=10)
                    )
                    st.plotly_chart(fig_ind, use_container_width=True)

                elif indicator == "TRIX":
                    dfi = ti.trix(df.copy(), horizon)
                    trix_col = next((c for c in dfi.columns if "trix" in c.lower()), None)
                    if trix_col:
                        st.line_chart(dfi.set_index("Date")[trix_col], color='#c084fc')
                    else:
                        st.write("TRIX column not found.")

                elif indicator == "ADX":
                    dfi = ti.average_directional_movement_index(df.copy(), 14)
                    adx_col = [c for c in dfi.columns if "adx" in c.lower()]
                    if adx_col:
                        st.line_chart(dfi.set_index("Date")[adx_col[0]], color='#10b981')
                    else:
                        st.write("ADX column not found.")

                elif indicator == "Mass Index":
                    dfi = ti.mass_index(df.copy())
                    mi_col = next((c for c in dfi.columns if "mass" in c.lower() or "mass index" in c.lower()), None)
                    if mi_col:
                        st.line_chart(dfi.set_index("Date")[mi_col], color='#f59e0b')
                    else:
                        st.write("Mass Index column not found.")

                # elif indicator == "KST Oscillator":
                #     r1, r2, r3, r4 = 10, 15, 20, 30
                #     n1, n2, n3, n4 = 10, 10, 10, 15
                #     dfi = ti.kst_oscillator(df.copy(), r1, r2, r3, r4, n1, n2, n3, n4)
                #     kst_col = [c for c in dfi.columns if "kst" in c.lower() and "signal" not in c.lower()]
                #     kst_signal_col = [c for c in dfi.columns if "kst" in c.lower() and "signal" in c.lower()]
                #     fig_ind = go.Figure()
                #     if kst_col:
                #         fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[kst_col[0]], name="KST", line=dict(color='#818cf8', width=2)))
                #     if kst_signal_col:
                #         fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[kst_signal_col[0]], name="Signal", line=dict(color='#f59
                else:
                    # fallback if an indicator is selected but not implemented
                    st.write(f"{indicator} is not implemented in the app or the TI module. Showing Close price instead.")
                    st.line_chart(df.set_index("Date")["Close"])

            except Exception as exc:
                st.write(f"Indicator plotting failed for {indicator}: {exc}")
