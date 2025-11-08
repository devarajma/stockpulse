# StockPulse

A simple Streamlit app to run a stock buy/wait predictor and visualize technical indicators.

## How to run

You can run StockPulse after cloning the repository or downloading a ZIP from GitHub.

1. Clone the repository (SSH or HTTPS):

```bash
# SSH
git clone git@github.com:yourusername/stockpulse.git

# or HTTPS
git clone https://github.com/yourusername/stockpulse.git
```

Or download the repository as a ZIP from GitHub and extract it.

2. Change into the project directory:

```bash
cd stockpulse
```

3. Create and activate a Python virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the Streamlit app:

```bash
streamlit run app.py
```

Then open your browser at:

```
http://localhost:8501
```

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
