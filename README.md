# godmode

Get responses from multiple LLMs at once to find the best answers to your questions

## Install the virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

## Run the app

```bash
python3 -m streamlit run app.py
```

### Run tests

```bash
python -m pytest
```
