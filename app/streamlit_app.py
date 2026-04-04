from __future__ import annotations

import os
from typing import Any

import httpx
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:3000")


@st.cache_data(ttl=300)
def fetch_data(year: int, limit: int, api_base_url: str) -> list[dict[str, Any]]:
    """Fetch education spending rows from the FastAPI backend."""
    url = f"{api_base_url.rstrip('/')}/api/education-spending"
    params = {"year": year, "limit": limit}

    response = httpx.get(url, params=params, timeout=20.0)
    response.raise_for_status()
    payload = response.json()
    return payload.get("data", [])


st.set_page_config(page_title="EdTech Insights", page_icon="📚", layout="wide")

st.title("EdTech Insights")
st.caption("Explore World Bank education spending (% of GDP) by country.")

with st.sidebar:
    st.header("Controls")
    api_base_url = st.text_input("API Base URL", value=API_BASE_URL)
    year = st.number_input("Year", min_value=1960,
                           max_value=2100, value=2022, step=1)
    limit = st.slider("Top N countries", min_value=5,
                      max_value=100, value=25, step=5)
    load = st.button("Load Data", type="primary")

if load:
    try:
        rows = fetch_data(year=year, limit=limit, api_base_url=api_base_url)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Could not load data from API: {exc}")
    else:
        if not rows:
            st.warning("No data returned for the selected year.")
        else:
            st.success(f"Loaded {len(rows)} rows")
            st.dataframe(rows, use_container_width=True)
else:
    st.info("Use the sidebar controls and click Load Data.")
