from fastapi import FastAPI

from app.schemas.analytics import GroupAnalysis, Summary
from app.services import analytics
from app.services.data_loader import get_frame

app = FastAPI(title="BIOPRESS Analytics", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/analytics/summary", response_model=Summary)
def get_summary():
    return analytics.summary(get_frame())


def _group_endpoint(dimension: str):
    def handler():
        return analytics.by_group(get_frame(), dimension)
    return handler


for _dim, _path in [("ward", "by-ward"), ("shift", "by-shift"), ("indication", "by-indication"), ("profcat", "by-profcat")]:
    app.add_api_route(f"/api/v1/analytics/{_path}", _group_endpoint(_dim), methods=["GET"], response_model=GroupAnalysis)
