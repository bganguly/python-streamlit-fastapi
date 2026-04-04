from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.services.worldbank import fetch_education_spending

app = FastAPI(title="EdTech Insights API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/indicators")
def indicators() -> dict[str, list[dict[str, str]]]:
    return {
        "items": [
            {
                "id": "SE.XPD.TOTL.GD.ZS",
                "name": "Government expenditure on education, total (% of GDP)",
                "source": "World Bank",
            }
        ]
    }


@app.get("/api/education-spending")
async def education_spending(
    year: int = Query(default=2022, ge=1960, le=2100),
    limit: int = Query(default=20, ge=1, le=100),
) -> dict[str, object]:
    results = await fetch_education_spending(year=year, limit=limit)
    return {
        "year": year,
        "count": len(results),
        "data": results,
    }


@app.get("/")
def home() -> FileResponse:
    return FileResponse(static_dir / "index.html")
