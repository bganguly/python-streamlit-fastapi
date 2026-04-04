# Python FastAPI EdTech

Short FastAPI + UI project using publicly accessible education data from the World Bank.

## Stack and entry points

- Backend: FastAPI
- UI option 1: Static HTML/CSS/JS served by FastAPI
- UI option 2: Streamlit app (`app/streamlit_app.py`)
- Data source: World Bank indicator API (public)
- API app entry: `app/main.py` (`app` object)
- Service layer: `app/services/worldbank.py`
- Tests: `tests/test_api.py`

## Quickstart

1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

3. Run the FastAPI backend + static UI

```bash
python -m uvicorn app.main:app --reload --port 3000
```

4. Open in browser

- http://127.0.0.1:3000
- Docs: http://127.0.0.1:3000/docs

## Run the Streamlit UI

In a second terminal, activate the same virtualenv first:

```bash
source .venv/bin/activate
```

Then run:

```bash
python -m streamlit run streamlit_app.py --server.port 8501
```

Alternative (equivalent):

```bash
python -m streamlit run app/streamlit_app.py --server.port 8501
```

Open: http://127.0.0.1:8501

### Troubleshooting

If you see `No module named streamlit`:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit --version
```

If activation is not convenient, run with the venv interpreter directly:

```bash
./.venv/bin/python -m streamlit run streamlit_app.py --server.port 8501
```

The Streamlit app calls the FastAPI endpoint at `http://127.0.0.1:3000/api/education-spending` by default.
You can override the API base URL with:

```bash
export API_BASE_URL="http://127.0.0.1:3000"
```

## Endpoints

- GET `/health`
- GET `/api/indicators`
- GET `/api/education-spending?year=2022&limit=25`
- GET `/`
