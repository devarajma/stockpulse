
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import technical_indicators as ti  # import your indicators
from utils import compute_final

# ==============================
# Streamlit App
# ==============================
st.set_page_config(page_title="Stock Predictor", layout="wide")
st.title("📈 Stock Buy or Wait Predictor")

# User inputs
ticker = st.text_input("Enter stock ticker (e.g., AAPL, TSLA, INFY.BO, RELIANCE.NS):", "AAPL")
horizon = st.slider("Prediction Horizon (days):", 1, 30, 5)

# ==============================
# Download Stock Data
# ==============================
def load_data(ticker):
    df = yf.download(ticker, period="1y", interval="1d")
    if df.empty:
        return pd.DataFrame()
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df.reset_index(inplace=True)
    return df

# ==============================
# Indicator Options
# ==============================
indicator_options = [
    "Moving Average (MA)",
    "Exponential Moving Average (EMA)",
    "Momentum",
    "Rate of Change (ROC)",
    "Average True Range (ATR)",
    "Bollinger Bands",
    "Pivot Points (PPSR)",
    "Stochastic Oscillator",
    "TRIX",
    # "ADX",
    "MACD",
    "Mass Index",
    # "Vortex Indicator",
    "KST Oscillator",
    "Relative Strength Index (RSI)",
    "True Strength Index (TSI)",
    "Accumulation/Distribution",
    "Chaikin Oscillator",
    "Money Flow Index (MFI)",
    "On Balance Volume (OBV)",
    "Force Index",
    "Ease of Movement (EoM)",
    "Commodity Channel Index (CCI)",
    "Coppock Curve",
    "Keltner Channel",
    "Ultimate Oscillator",
    "Donchian Channel",
    "Standard Deviation"
]



selected_indicators = st.multiselect("📊 Select Technical Indicators", indicator_options, default=["MACD"])

# ==============================
# Prediction + Charts
# ==============================
if st.button("Run Analysis"):
    df = load_data(ticker)

    if df.empty:
        st.error("❌ No data found for this ticker.")
    else:
        # --- Prediction
        prob = compute_final(ticker, horizon)
        if prob >= 0.6:
            signal = "BUY ✅"
            color = "green"
        else:
            signal = "WAIT ⏳"
            color = "red"

        st.subheader(f"Prediction for {ticker}: **:{color}[{signal}]** (prob = {prob:.2f})")

        # --- Candlestick Chart
        fig_candle = go.Figure(data=[go.Candlestick(
            x=df['Date'],
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'],
            name="Candlestick"
        )])
        fig_candle.update_layout(title=f"{ticker} - Last 1 Year", xaxis_rangeslider_visible=False, template="plotly_dark")
        st.plotly_chart(fig_candle, use_container_width=True)

        # --- Plot Selected Indicators ---
        for indicator in selected_indicators:
            st.markdown(f"### 📈 {indicator}")
            fig = go.Figure()

            if indicator == "Moving Average (MA)":
                df = ti.moving_average(df, 20)
                fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_20'], mode='lines', name='MA 20'))

            elif indicator == "Exponential Moving Average (EMA)":
                df = ti.exponential_moving_average(df, 20)
                fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA_20'], mode='lines', name='EMA 20'))

            elif indicator == "Momentum":
                df = ti.momentum(df, 10)
                fig.add_trace(go.Scatter(x=df['Date'], y=df['Momentum_10'], mode='lines', name='Momentum'))

            elif indicator == "Rate of Change (ROC)":
                df = ti.rate_of_change(df, 10)
                fig.add_trace(go.Scatter(x=df['Date'], y=df['ROC_10'], mode='lines', name='ROC'))
            elif indicator == "Average True Range (ATR)":
                df = ti.average_true_range(df, 14)
                fig.add_trace(go.Scatter(x=df['Date'], y=df['ATR_14'], mode='lines', name='ATR'))

            elif indicator == "Bollinger Bands":
                df = ti.bollinger_bands(df, 20)
                fig.add_trace(go.Scatter(x=df['Date'], y=df['BollingerB_20'], mode='lines', name='BollingerB'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['Bollinger%b_20'], mode='lines', name='Bollinger%b'))

            elif indicator == "Pivot Points (PPSR)":
                df = ti.ppsr(df)  # compute Pivot Points
                fig.add_trace(go.Scatter(x=df['Date'], y=df['PP'], mode='lines', name='Pivot Point'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['S1'], mode='lines', name='Support 1'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['R1'], mode='lines', name='Resistance 1'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['S2'], mode='lines', name='Support 2'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['R2'], mode='lines', name='Resistance 2'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['S3'], mode='lines', name='Support 3'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['R3'], mode='lines', name='Resistance 3'))


            elif indicator == "Stochastic Oscillator":
                df = ti.stochastic_oscillator_d(df, horizon)
                fig.add_trace(go.Scatter(x=df['Date'], y=df[f'SO%K_{horizon}'], mode='lines', name='%K'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df[f'SO%D_{horizon}'], mode='lines', name='%D'))


            elif indicator == "TRIX":
                df = ti.trix(df, horizon)  # horizon or your chosen period
                trix_col = f'Trix_{horizon}'  # match the column name generated by function
                fig.add_trace(go.Scatter(x=df['Date'], y=df[trix_col], mode='lines', name='TRIX'))

            elif indicator == "ADX":
                df = ti.average_directional_movement_index(df, 14)
                fig.add_trace(go.Scatter(x=df['Date'], y=df['ADX_14'], mode='lines', name='ADX'))

            elif indicator == "MACD":
                df = ti.macd(df, 12, 26)
                fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD_12_26'], mode='lines', name='MACD'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['MACDsign_12_26'], mode='lines', name='Signal'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['MACDdiff_12_26'], mode='lines', name='MACD diff'))

            elif indicator == "Mass Index":
                df = ti.mass_index(df)  # no extra parameters
                fig.add_trace(go.Scatter(x=df['Date'], y=df['Mass Index'], mode='lines', name='Mass Index'))


            # elif indicator == "Vortex Indicator":
            #     df = ti.vortex_indicator(df, horizon)
            #     fig.add_trace(go.Scatter(x=df['Date'], y=df[f'VI_plus_{horizon}'], mode='lines', name='VI+'))
            #     fig.add_trace(go.Scatter(x=df['Date'], y=df[f'VI_minus_{horizon}'], mode='lines', name='VI-'))



            elif indicator == "KST Oscillator":
                r1, r2, r3, r4 = 10, 15, 20, 30
                n1, n2, n3, n4 = 10, 10, 10, 15
                df = ti.kst_oscillator(df, r1, r2, r3, r4, n1, n2, n3, n4)

                kst_col = f'KST_{r1}_{r2}_{r3}_{r4}_{n1}_{n2}_{n3}_{n4}'
                kst_signal_col = f'KST_signal_{r1}_{r2}_{r3}_{r4}_{n1}_{n2}_{n3}_{n4}'

                # Create a signal line (9-period EMA of KST)
                df[kst_signal_col] = df[kst_col].ewm(span=9, min_periods=9).mean()

                fig.add_trace(go.Scatter(x=df['Date'], y=df[kst_col], mode='lines', name='KST'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df[kst_signal_col], mode='lines', name='KST Signal'))


            elif indicator == "Relative Strength Index (RSI)":
                df = ti.relative_strength_index(df, horizon)
                fig.add_trace(go.Scatter(x=df['Date'], y=df[f'RSI_{horizon}'], mode='lines', name='RSI'))


            elif indicator == "True Strength Index (TSI)":
                df = ti.true_strength_index(df, 25, 13)
                fig.add_trace(go.Scatter(x=df['Date'], y=df['TSI_25_13'], mode='lines', name='TSI'))

            elif indicator == "Accumulation/Distribution":
                n = horizon  # or any default period you want
                df = ti.accumulation_distribution(df, n)
                fig.add_trace(go.Scatter(x=df['Date'], y=df[f'Acc/Dist_ROC_{n}'], mode='lines', name='Accumulation/Distribution'))


            elif indicator == "Chaikin Oscillator":
                df = ti.chaikin_oscillator(df)
                fig.add_trace(go.Scatter(
                    x=df['Date'], 
                    y=df['Chaikin'], 
                    mode='lines', 
                    name='Chaikin Oscillator'
                ))

            elif indicator == "Money Flow Index (MFI)":
                df = ti.money_flow_index(df, horizon)  # horizon or desired period
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[f'MFI_{horizon}'],
                    mode='lines',
                    name=f'MFI_{horizon}'
                ))

            elif indicator == "On Balance Volume (OBV)":
                df = ti.on_balance_volume(df, horizon)  # horizon or desired period
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[f'OBV_{horizon}'],
                    mode='lines',
                    name=f'OBV_{horizon}'
                ))

            elif indicator == "Force Index":
                df = ti.force_index(df, horizon)  # horizon or desired period
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[f'Force_{horizon}'],
                    mode='lines',
                    name=f'Force Index_{horizon}'
                ))

            elif indicator == "Commodity Channel Index (CCI)":
                df = ti.commodity_channel_index(df, 20)
                fig.add_trace(go.Scatter(x=df['Date'], y=df['CCI_20'], mode='lines', name='CCI'))

            elif indicator == "Coppock Curve":
                df = ti.coppock_curve(df, horizon)  # horizon is the period 'n'
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[f'Copp_{horizon}'],
                    mode='lines',
                    name=f'Coppock Curve_{horizon}'
                ))

            elif indicator == "Keltner Channel":
                df = ti.keltner_channel(df, horizon)
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[f'KelChM_{horizon}'],
                    mode='lines',
                    name=f'Keltner Middle_{horizon}'
                ))
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[f'KelChU_{horizon}'],
                    mode='lines',
                    name=f'Keltner Upper_{horizon}'
                ))
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[f'KelChD_{horizon}'],
                    mode='lines',
                    name=f'Keltner Lower_{horizon}'
                ))

            elif indicator == "Ultimate Oscillator":
                df = ti.ultimate_oscillator(df)
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df['Ultimate_Osc'],
                    mode='lines',
                    name='Ultimate Oscillator'
                ))


            elif indicator == "Donchian Channel":
                df = ti.donchian_channel(df, horizon)
                fig.add_trace(go.Scatter(x=df['Date'], y=df[f'Donchian_{horizon}'], mode='lines', name=f'Donchian Channel_{horizon}'))



            elif indicator == "Standard Deviation":
                df = ti.standard_deviation(df, horizon)
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[f'STD_{horizon}'],
                    mode='lines',
                    name=f'Standard Deviation_{horizon}'
                ))

            elif indicator == "Ease of Movement (EoM)":
                df = ti.ease_of_movement(df, horizon)
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[f'EoM_{horizon}'],
                    mode='lines',
                    name=f'Ease of Movement_{horizon}'
                ))

            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
