from __future__ import annotations

from typing import Any

import httpx

WORLD_BANK_API = "https://api.worldbank.org/v2"
ED_SPENDING_INDICATOR = "SE.XPD.TOTL.GD.ZS"


async def fetch_education_spending(year: int = 2022, limit: int = 20) -> list[dict[str, Any]]:
    """Fetch education spending (% of GDP) by country for a given year."""
    url = f"{WORLD_BANK_API}/country/all/indicator/{ED_SPENDING_INDICATOR}"
    params = {
        "format": "json",
        "date": str(year),
        "per_page": 400,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        payload = response.json()

    entries = payload[1] if isinstance(
        payload, list) and len(payload) > 1 else []
    normalized: list[dict[str, Any]] = []

    for row in entries:
        value = row.get("value")
        country = row.get("country", {})
        name = country.get("value")

        if value is None or not name:
            continue

        normalized.append(
            {
                "country": name,
                "country_code": row.get("countryiso3code"),
                "year": row.get("date"),
                "education_spending_pct_gdp": value,
            }
        )

    normalized.sort(
        key=lambda item: item["education_spending_pct_gdp"], reverse=True)
    return normalized[:limit]
