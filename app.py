
# import streamlit as st
# import yfinance as yf
# import pandas as pd
# import plotly.graph_objects as go
# import technical_indicators as ti  # import your indicators
# from utils import compute_final

# # ==============================
# # Streamlit App
# # ==============================
# st.set_page_config(page_title="Stock Predictor", layout="wide")
# st.title("📈 Stock Buy or Wait Predictor")

# # User inputs
# ticker = st.text_input("Enter stock ticker (e.g., AAPL, TSLA, INFY.BO, RELIANCE.NS):", "AAPL")
# horizon = st.slider("Prediction Horizon (days):", 1, 30, 5)

# # ==============================
# # Download Stock Data
# # ==============================
# def load_data(ticker):
#     df = yf.download(ticker, period="1y", interval="1d")
#     if df.empty:
#         return pd.DataFrame()
#     df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
#     df.reset_index(inplace=True)
#     return df

# # ==============================
# # Indicator Options
# # ==============================
# indicator_options = [
#     "Moving Average (MA)",
#     "Exponential Moving Average (EMA)",
#     "Momentum",
#     "Rate of Change (ROC)",
#     "Average True Range (ATR)",
#     "Bollinger Bands",
#     "Pivot Points (PPSR)",
#     "Stochastic Oscillator",
#     "TRIX",
#     # "ADX",
#     "MACD",
#     "Mass Index",
#     # "Vortex Indicator",
#     "KST Oscillator",
#     "Relative Strength Index (RSI)",
#     "True Strength Index (TSI)",
#     "Accumulation/Distribution",
#     "Chaikin Oscillator",
#     "Money Flow Index (MFI)",
#     "On Balance Volume (OBV)",
#     "Force Index",
#     "Ease of Movement (EoM)",
#     "Commodity Channel Index (CCI)",
#     "Coppock Curve",
#     "Keltner Channel",
#     "Ultimate Oscillator",
#     "Donchian Channel",
#     "Standard Deviation"
# ]



# selected_indicators = st.multiselect("📊 Select Technical Indicators", indicator_options, default=["MACD"])

# # ==============================
# # Prediction + Charts
# # ==============================
# if st.button("Run Analysis"):
#     df = load_data(ticker)

#     if df.empty:
#         st.error("❌ No data found for this ticker.")
#     else:
#         # --- Prediction
#         prob = compute_final(ticker, horizon)
#         if prob >= 0.6:
#             signal = "BUY ✅"
#             color = "green"
#         else:
#             signal = "WAIT ⏳"
#             color = "red"

#         st.subheader(f"Prediction for {ticker}: **:{color}[{signal}]** (prob = {prob:.2f})")

#         # --- Candlestick Chart
#         fig_candle = go.Figure(data=[go.Candlestick(
#             x=df['Date'],
#             open=df['Open'], high=df['High'],
#             low=df['Low'], close=df['Close'],
#             name="Candlestick"
#         )])
#         fig_candle.update_layout(title=f"{ticker} - Last 1 Year", xaxis_rangeslider_visible=False, template="plotly_dark")
#         st.plotly_chart(fig_candle, use_container_width=True)

#         # --- Plot Selected Indicators ---
#         for indicator in selected_indicators:
#             st.markdown(f"### 📈 {indicator}")
#             fig = go.Figure()

#             if indicator == "Moving Average (MA)":
#                 df = ti.moving_average(df, 20)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_20'], mode='lines', name='MA 20'))

#             elif indicator == "Exponential Moving Average (EMA)":
#                 df = ti.exponential_moving_average(df, 20)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA_20'], mode='lines', name='EMA 20'))

#             elif indicator == "Momentum":
#                 df = ti.momentum(df, 10)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['Momentum_10'], mode='lines', name='Momentum'))

#             elif indicator == "Rate of Change (ROC)":
#                 df = ti.rate_of_change(df, 10)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['ROC_10'], mode='lines', name='ROC'))
#             elif indicator == "Average True Range (ATR)":
#                 df = ti.average_true_range(df, 14)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['ATR_14'], mode='lines', name='ATR'))

#             elif indicator == "Bollinger Bands":
#                 df = ti.bollinger_bands(df, 20)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['BollingerB_20'], mode='lines', name='BollingerB'))
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['Bollinger%b_20'], mode='lines', name='Bollinger%b'))

#             elif indicator == "Pivot Points (PPSR)":
#                 df = ti.ppsr(df)  # compute Pivot Points
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['PP'], mode='lines', name='Pivot Point'))
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['S1'], mode='lines', name='Support 1'))
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['R1'], mode='lines', name='Resistance 1'))
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['S2'], mode='lines', name='Support 2'))
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['R2'], mode='lines', name='Resistance 2'))
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['S3'], mode='lines', name='Support 3'))
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['R3'], mode='lines', name='Resistance 3'))


#             elif indicator == "Stochastic Oscillator":
#                 df = ti.stochastic_oscillator_d(df, horizon)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df[f'SO%K_{horizon}'], mode='lines', name='%K'))
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df[f'SO%D_{horizon}'], mode='lines', name='%D'))


#             elif indicator == "TRIX":
#                 df = ti.trix(df, horizon)  # horizon or your chosen period
#                 trix_col = f'Trix_{horizon}'  # match the column name generated by function
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df[trix_col], mode='lines', name='TRIX'))

#             elif indicator == "ADX":
#                 df = ti.average_directional_movement_index(df, 14)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['ADX_14'], mode='lines', name='ADX'))

#             elif indicator == "MACD":
#                 df = ti.macd(df, 12, 26)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD_12_26'], mode='lines', name='MACD'))
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['MACDsign_12_26'], mode='lines', name='Signal'))
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['MACDdiff_12_26'], mode='lines', name='MACD diff'))

#             elif indicator == "Mass Index":
#                 df = ti.mass_index(df)  # no extra parameters
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['Mass Index'], mode='lines', name='Mass Index'))


#             # elif indicator == "Vortex Indicator":
#             #     df = ti.vortex_indicator(df, horizon)
#             #     fig.add_trace(go.Scatter(x=df['Date'], y=df[f'VI_plus_{horizon}'], mode='lines', name='VI+'))
#             #     fig.add_trace(go.Scatter(x=df['Date'], y=df[f'VI_minus_{horizon}'], mode='lines', name='VI-'))



#             elif indicator == "KST Oscillator":
#                 r1, r2, r3, r4 = 10, 15, 20, 30
#                 n1, n2, n3, n4 = 10, 10, 10, 15
#                 df = ti.kst_oscillator(df, r1, r2, r3, r4, n1, n2, n3, n4)

#                 kst_col = f'KST_{r1}_{r2}_{r3}_{r4}_{n1}_{n2}_{n3}_{n4}'
#                 kst_signal_col = f'KST_signal_{r1}_{r2}_{r3}_{r4}_{n1}_{n2}_{n3}_{n4}'

#                 # Create a signal line (9-period EMA of KST)
#                 df[kst_signal_col] = df[kst_col].ewm(span=9, min_periods=9).mean()

#                 fig.add_trace(go.Scatter(x=df['Date'], y=df[kst_col], mode='lines', name='KST'))
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df[kst_signal_col], mode='lines', name='KST Signal'))


#             elif indicator == "Relative Strength Index (RSI)":
#                 df = ti.relative_strength_index(df, horizon)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df[f'RSI_{horizon}'], mode='lines', name='RSI'))


#             elif indicator == "True Strength Index (TSI)":
#                 df = ti.true_strength_index(df, 25, 13)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['TSI_25_13'], mode='lines', name='TSI'))

#             elif indicator == "Accumulation/Distribution":
#                 n = horizon  # or any default period you want
#                 df = ti.accumulation_distribution(df, n)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df[f'Acc/Dist_ROC_{n}'], mode='lines', name='Accumulation/Distribution'))


#             elif indicator == "Chaikin Oscillator":
#                 df = ti.chaikin_oscillator(df)
#                 fig.add_trace(go.Scatter(
#                     x=df['Date'], 
#                     y=df['Chaikin'], 
#                     mode='lines', 
#                     name='Chaikin Oscillator'
#                 ))

#             elif indicator == "Money Flow Index (MFI)":
#                 df = ti.money_flow_index(df, horizon)  # horizon or desired period
#                 fig.add_trace(go.Scatter(
#                     x=df['Date'],
#                     y=df[f'MFI_{horizon}'],
#                     mode='lines',
#                     name=f'MFI_{horizon}'
#                 ))

#             elif indicator == "On Balance Volume (OBV)":
#                 df = ti.on_balance_volume(df, horizon)  # horizon or desired period
#                 fig.add_trace(go.Scatter(
#                     x=df['Date'],
#                     y=df[f'OBV_{horizon}'],
#                     mode='lines',
#                     name=f'OBV_{horizon}'
#                 ))

#             elif indicator == "Force Index":
#                 df = ti.force_index(df, horizon)  # horizon or desired period
#                 fig.add_trace(go.Scatter(
#                     x=df['Date'],
#                     y=df[f'Force_{horizon}'],
#                     mode='lines',
#                     name=f'Force Index_{horizon}'
#                 ))

#             elif indicator == "Commodity Channel Index (CCI)":
#                 df = ti.commodity_channel_index(df, 20)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df['CCI_20'], mode='lines', name='CCI'))

#             elif indicator == "Coppock Curve":
#                 df = ti.coppock_curve(df, horizon)  # horizon is the period 'n'
#                 fig.add_trace(go.Scatter(
#                     x=df['Date'],
#                     y=df[f'Copp_{horizon}'],
#                     mode='lines',
#                     name=f'Coppock Curve_{horizon}'
#                 ))

#             elif indicator == "Keltner Channel":
#                 df = ti.keltner_channel(df, horizon)
#                 fig.add_trace(go.Scatter(
#                     x=df['Date'],
#                     y=df[f'KelChM_{horizon}'],
#                     mode='lines',
#                     name=f'Keltner Middle_{horizon}'
#                 ))
#                 fig.add_trace(go.Scatter(
#                     x=df['Date'],
#                     y=df[f'KelChU_{horizon}'],
#                     mode='lines',
#                     name=f'Keltner Upper_{horizon}'
#                 ))
#                 fig.add_trace(go.Scatter(
#                     x=df['Date'],
#                     y=df[f'KelChD_{horizon}'],
#                     mode='lines',
#                     name=f'Keltner Lower_{horizon}'
#                 ))

#             elif indicator == "Ultimate Oscillator":
#                 df = ti.ultimate_oscillator(df)
#                 fig.add_trace(go.Scatter(
#                     x=df['Date'],
#                     y=df['Ultimate_Osc'],
#                     mode='lines',
#                     name='Ultimate Oscillator'
#                 ))


#             elif indicator == "Donchian Channel":
#                 df = ti.donchian_channel(df, horizon)
#                 fig.add_trace(go.Scatter(x=df['Date'], y=df[f'Donchian_{horizon}'], mode='lines', name=f'Donchian Channel_{horizon}'))



#             elif indicator == "Standard Deviation":
#                 df = ti.standard_deviation(df, horizon)
#                 fig.add_trace(go.Scatter(
#                     x=df['Date'],
#                     y=df[f'STD_{horizon}'],
#                     mode='lines',
#                     name=f'Standard Deviation_{horizon}'
#                 ))

#             elif indicator == "Ease of Movement (EoM)":
#                 df = ti.ease_of_movement(df, horizon)
#                 fig.add_trace(go.Scatter(
#                     x=df['Date'],
#                     y=df[f'EoM_{horizon}'],
#                     mode='lines',
#                     name=f'Ease of Movement_{horizon}'
#                 ))

#             fig.update_layout(template="plotly_white")
#             st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import technical_indicators as ti  # your custom indicators module
from utils import compute_final

# ------------------------------
# Page config + styling
# ------------------------------
st.set_page_config(page_title="StockPulse — Stock Predictor", layout="wide")

st.markdown(
    """
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:6px;padding:10px;">
    <div style="font-size:46px;font-weight:800;letter-spacing:1px">StockPulse</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
  .stApp { background: linear-gradient(180deg, #071024 0%, #031923 100%); }
  .stBlock > div { color: #e6eef8; }
  .metric-box { padding: 12px 16px; border-radius: 8px; background: rgba(255,255,255,0.03); }
  .prediction { font-size:20px; font-weight:700; }
  .signal-buy { color: #16a34a; }
  .signal-wait { color: #f97316; }
  .card { background: rgba(255,255,255,0.02); border-radius: 8px; padding: 12px; }
</style>
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
    # handle yfinance multi-index columns in some versions
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df = df.reset_index()  # Date becomes a column
    return df

# ------------------------------
# Sidebar controls
# ------------------------------
with st.sidebar:
    st.header("Controls")
    ticker = st.text_input("Ticker (e.g. AAPL, TSLA, INFY.BO, RELIANCE.NS)", "AAPL")
    horizon = st.slider("Prediction horizon (days)", 1, 30, 5)
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
        "TRSI",  # keep as placeholder if you have this
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
    selected_indicators = st.multiselect("Select indicators", indicator_options, default=["MACD"])
    run = st.button("Run Analysis")

# ------------------------------
# Main app logic
# ------------------------------
if run:
    df = load_data(ticker)
    if df.empty:
        st.error("No data found for this ticker — try a different symbol.")
    else:
        # prediction (safe fallback on error)
        try:
            prob = float(compute_final(ticker, horizon))
        except Exception as e:
            st.warning(f"Prediction failed, defaulting probability to 0.0 ({e})")
            prob = 0.0

        signal = "BUY ✅" if prob >= 0.6 else "WAIT ⏳"
        badge_class = "signal-buy" if prob >= 0.6 else "signal-wait"

        # layout: left (metrics), right (charts)
        left, right = st.columns([1, 3])
        with left:
            st.markdown(
                f"""
                <div class="metric-box">
                  <div class="prediction {badge_class}">{signal}</div>
                  <div style="opacity:0.9">Probability: {prob:.2f}</div>
                  <div style="margin-top:8px;font-size:12px;opacity:0.8">Horizon: {horizon} days</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:
            st.write(f"### {ticker} — Last 1 Year")

            # Candlestick figure
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=df["Date"],
                        open=df["Open"],
                        high=df["High"],
                        low=df["Low"],
                        close=df["Close"],
                        name="Price",
                    )
                ]
            )
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=500)
            st.plotly_chart(fig, use_container_width=True)

        # ------------------------------
        # Indicators: process each selection
        # ------------------------------
        for indicator in selected_indicators:
            st.markdown(f"### {indicator}")
            try:
                # MACD example: ti.macd returns a dataframe with columns MACD_12_26, MACDsign_12_26, MACDdiff_12_26
                if indicator == "MACD":
                    dfi = ti.macd(df.copy(), 12, 26)
                    fig_ind = go.Figure()
                    fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["MACD_12_26"], name="MACD"))
                    fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["MACDsign_12_26"], name="Signal"))
                    fig_ind.add_trace(go.Bar(x=dfi["Date"], y=dfi["MACDdiff_12_26"], name="MACD diff"))
                    fig_ind.update_layout(template="plotly_dark", height=350)
                    st.plotly_chart(fig_ind, use_container_width=True)

                elif indicator == "RSI":
                    dfi = ti.relative_strength_index(df.copy(), 14)
                    # ensure RSI column exists
                    rsi_col = [c for c in dfi.columns if c.lower().startswith("rsi")]
                    if rsi_col:
                        st.line_chart(dfi.set_index("Date")[rsi_col[0]])
                    else:
                        st.write("RSI calculation did not return expected column.")

                elif indicator == "Momentum":
                    dfi = ti.momentum(df.copy(), 10)
                    mom_col = [c for c in dfi.columns if "momentum" in c.lower() or "moment" in c.lower()]
                    if mom_col:
                        st.line_chart(dfi.set_index("Date")[mom_col[0]])
                    else:
                        st.write("Momentum function did not return expected column.")

                elif indicator == "Bollinger Bands":
                    dfi = ti.bollinger_bands(df.copy(), 20)
                    fig_ind = go.Figure()
                    fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["BB_Middle"], name="Middle"))
                    fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["BB_Upper"], name="Upper"))
                    fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi["BB_Lower"], name="Lower"))
                    fig_ind.update_layout(template="plotly_dark", height=350)
                    st.plotly_chart(fig_ind, use_container_width=True)

                elif indicator == "ATR":
                    dfi = ti.average_true_range(df.copy(), 14)
                    atr_col = [c for c in dfi.columns if "atr" in c.lower()]
                    if atr_col:
                        st.line_chart(dfi.set_index("Date")[atr_col[0]])
                    else:
                        st.write("ATR did not return expected column.")

                elif indicator == "OBV" or indicator == "On Balance Volume (OBV)":
                    dfi = ti.on_balance_volume(df.copy(), horizon)
                    obv_col = [c for c in dfi.columns if "obv" in c.lower()]
                    if obv_col:
                        st.line_chart(dfi.set_index("Date")[obv_col[0]])
                    else:
                        # fallback to computing simple OBV if function missing
                        st.write("OBV function didn't return expected column. Plotting Close price as fallback.")
                        st.line_chart(df.set_index("Date")["Close"])

                elif indicator == "Pivot Points (PPSR)":
                    dfi = ti.ppsr(df.copy())
                    fig_ind = go.Figure()
                    for name in ["PP", "S1", "R1", "S2", "R2", "S3", "R3"]:
                        if name in dfi.columns:
                            fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[name], mode="lines", name=name))
                    fig_ind.update_layout(template="plotly_dark", height=350)
                    st.plotly_chart(fig_ind, use_container_width=True)

                elif indicator == "Stochastic Oscillator":
                    dfi = ti.stochastic_oscillator_d(df.copy(), horizon)
                    k_col = next((c for c in dfi.columns if "%K" in c or "so%k" in c.lower()), None)
                    d_col = next((c for c in dfi.columns if "%D" in c or "so%d" in c.lower()), None)
                    fig_ind = go.Figure()
                    if k_col:
                        fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[k_col], name="%K"))
                    if d_col:
                        fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[d_col], name="%D"))
                    fig_ind.update_layout(template="plotly_dark", height=350)
                    st.plotly_chart(fig_ind, use_container_width=True)

                elif indicator == "TRIX":
                    dfi = ti.trix(df.copy(), horizon)
                    trix_col = next((c for c in dfi.columns if "trix" in c.lower()), None)
                    if trix_col:
                        st.line_chart(dfi.set_index("Date")[trix_col])
                    else:
                        st.write("TRIX column not found.")

                elif indicator == "ADX":
                    dfi = ti.average_directional_movement_index(df.copy(), 14)
                    adx_col = [c for c in dfi.columns if "adx" in c.lower()]
                    if adx_col:
                        st.line_chart(dfi.set_index("Date")[adx_col[0]])
                    else:
                        st.write("ADX column not found.")

                elif indicator == "Mass Index":
                    dfi = ti.mass_index(df.copy())
                    mi_col = next((c for c in dfi.columns if "mass" in c.lower() or "mass index" in c.lower()), None)
                    if mi_col:
                        st.line_chart(dfi.set_index("Date")[mi_col])
                    else:
                        st.write("Mass Index column not found.")

                elif indicator == "KST Oscillator":
                    # example parameters (you can expose these in sidebar if needed)
                    r1, r2, r3, r4 = 10, 15, 20, 30
                    n1, n2, n3, n4 = 10, 10, 10, 15
                    dfi = ti.kst_oscillator(df.copy(), r1, r2, r3, r4, n1, n2, n3, n4)
                    kst_col = [c for c in dfi.columns if "kst" in c.lower() and "signal" not in c.lower()]
                    kst_signal_col = [c for c in dfi.columns if "kst" in c.lower() and "signal" in c.lower()]
                    fig_ind = go.Figure()
                    if kst_col:
                        fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[kst_col[0]], name="KST"))
                    if kst_signal_col:
                        fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[kst_signal_col[0]], name="KST Signal"))
                    fig_ind.update_layout(template="plotly_dark", height=350)
                    st.plotly_chart(fig_ind, use_container_width=True)

                elif indicator in ("TSI", "True Strength Index (TSI)"):
                    dfi = ti.true_strength_index(df.copy(), 25, 13)
                    tsi_col = next((c for c in dfi.columns if "tsi" in c.lower()), None)
                    if tsi_col:
                        st.line_chart(dfi.set_index("Date")[tsi_col])
                    else:
                        st.write("TSI column not found.")

                elif indicator == "Accumulation/Distribution":
                    dfi = ti.accumulation_distribution(df.copy(), horizon)
                    acc_col = next((c for c in dfi.columns if "acc" in c.lower() or "acc/dist" in c.lower()), None)
                    if acc_col:
                        st.line_chart(dfi.set_index("Date")[acc_col])
                    else:
                        st.write("Accumulation/Distribution column not found.")

                elif indicator == "Chaikin Oscillator":
                    dfi = ti.chaikin_oscillator(df.copy())
                    chaikin_col = next((c for c in dfi.columns if "chaikin" in c.lower()), None)
                    if chaikin_col:
                        st.line_chart(dfi.set_index("Date")[chaikin_col])
                    else:
                        st.write("Chaikin column not found.")

                elif indicator == "Money Flow Index (MFI)":
                    dfi = ti.money_flow_index(df.copy(), horizon)
                    mfi_col = next((c for c in dfi.columns if "mfi" in c.lower()), None)
                    if mfi_col:
                        st.line_chart(dfi.set_index("Date")[mfi_col])
                    else:
                        st.write("MFI column not found.")

                elif indicator == "Force Index":
                    dfi = ti.force_index(df.copy(), horizon)
                    f_col = next((c for c in dfi.columns if "force" in c.lower()), None)
                    if f_col:
                        st.line_chart(dfi.set_index("Date")[f_col])
                    else:
                        st.write("Force Index column not found.")

                elif indicator == "CCI" or indicator == "Commodity Channel Index (CCI)":
                    dfi = ti.commodity_channel_index(df.copy(), 20)
                    cci_col = next((c for c in dfi.columns if "cci" in c.lower()), None)
                    if cci_col:
                        st.line_chart(dfi.set_index("Date")[cci_col])
                    else:
                        st.write("CCI column not found.")

                elif indicator == "Coppock Curve":
                    dfi = ti.coppock_curve(df.copy(), horizon)
                    copp_col = next((c for c in dfi.columns if "copp" in c.lower()), None)
                    if copp_col:
                        st.line_chart(dfi.set_index("Date")[copp_col])
                    else:
                        st.write("Coppock column not found.")

                elif indicator == "Keltner Channel":
                    dfi = ti.keltner_channel(df.copy(), horizon)
                    keys = [k for k in dfi.columns if "kelch" in k.lower() or "kelt" in k.lower()]
                    fig_ind = go.Figure()
                    for key in keys:
                        fig_ind.add_trace(go.Scatter(x=dfi["Date"], y=dfi[key], name=key))
                    fig_ind.update_layout(template="plotly_dark", height=350)
                    st.plotly_chart(fig_ind, use_container_width=True)

                elif indicator == "Ultimate Oscillator":
                    dfi = ti.ultimate_oscillator(df.copy())
                    u_col = next((c for c in dfi.columns if "ultimate" in c.lower() or "ultimate_osc" in c.lower()), None)
                    if u_col:
                        st.line_chart(dfi.set_index("Date")[u_col])
                    else:
                        st.write("Ultimate Oscillator column not found.")

                elif indicator == "Donchian Channel":
                    dfi = ti.donchian_channel(df.copy(), horizon)
                    don_col = next((c for c in dfi.columns if "donchian" in c.lower()), None)
                    if don_col:
                        st.line_chart(dfi.set_index("Date")[don_col])
                    else:
                        st.write("Donchian column not found.")

                elif indicator == "Standard Deviation":
                    dfi = ti.standard_deviation(df.copy(), horizon)
                    std_col = next((c for c in dfi.columns if "std" in c.lower()), None)
                    if std_col:
                        st.line_chart(dfi.set_index("Date")[std_col])
                    else:
                        st.write("Standard Deviation column not found.")

                elif indicator == "Ease of Movement (EoM)":
                    dfi = ti.ease_of_movement(df.copy(), horizon)
                    eom_col = next((c for c in dfi.columns if "eom" in c.lower() or "ease" in c.lower()), None)
                    if eom_col:
                        st.line_chart(dfi.set_index("Date")[eom_col])
                    else:
                        st.write("Ease of Movement column not found.")

                else:
                    # fallback if an indicator is selected but not implemented
                    st.write(f"{indicator} is not implemented in the app or the TI module. Showing Close price instead.")
                    st.line_chart(df.set_index("Date")["Close"])

            except Exception as exc:
                st.write(f"Indicator plotting failed for {indicator}: {exc}")
