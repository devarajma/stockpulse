# StockPulse

A simple Streamlit app to run a stock buy/wait predictor and visualize technical indicators.

## Run locally

Follow the steps below to run the app locally (zsh):

1. Activate the venv (optional but recommended)

If you already have the venv created at `.venv`, activate it:

```bash
source /Users/devarajanma/stock_pulse/.venv/bin/activate
```

If you don't have a venv and want to create one:

```bash
cd /Users/devarajanma/stock_pulse
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies (if not already installed)

```bash
pip install -r /Users/devarajanma/stock_pulse/requirements.txt
```

(Or install specific packages:)

```bash
pip install streamlit yfinance pandas numpy scikit-learn plotly
```

3. Run the Streamlit app

```bash
streamlit run /Users/devarajanma/stock_pulse/app.py
```

or explicitly via the venv Python:

```bash
/Users/devarajanma/stock_pulse/.venv/bin/python -m streamlit run /Users/devarajanma/stock_pulse/app.py
```

4. Open the app in your browser

- Visit: http://localhost:8501

## Troubleshooting

- If the browser shows an error "No module named ...", make sure the venv is activated and you installed packages into that venv (use `which python` / `which pip` to confirm).
- To improve reload performance on macOS, install watchdog:

```bash
pip install watchdog
xcode-select --install   # if prompted for developer tools (macOS)
```

- If port 8501 is already used, start Streamlit on another port:

```bash
streamlit run app.py --server.port 8502
```

- If your app references local modules (like `technical_indicators.py` and `utils.py`), ensure they are importable (they're in the project root, so they should be fine). If you see import errors, paste them here and I’ll fix them.

## License

Add a license if needed.
