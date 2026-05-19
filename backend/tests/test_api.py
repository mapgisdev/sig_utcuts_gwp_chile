"""Backend tests for SIG-UTCUTS Chile."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_dashboard_summary():
    r = client.get("/api/v1/dashboard/summary")
    assert r.status_code == 200
    data = r.json()
    assert "total_investment_usd" in data
    assert "mechanisms_count" in data


def test_list_mechanisms():
    r = client.get("/api/v1/mechanisms")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_list_territories():
    r = client.get("/api/v1/territories?type=region")
    assert r.status_code == 200


def test_list_investments():
    r = client.get("/api/v1/investments")
    assert r.status_code == 200


def test_prioritization_ranking():
    r = client.get("/api/v1/prioritization/ranking")
    assert r.status_code == 200


def test_mrv_indicators():
    r = client.get("/api/v1/mrv/indicators")
    assert r.status_code == 200


def test_mrv_summary():
    r = client.get("/api/v1/mrv/summary")
    assert r.status_code == 200


def test_data_quality_summary():
    r = client.get("/api/v1/data-quality/summary")
    assert r.status_code == 200


def test_national_report():
    r = client.get("/api/v1/reports/national")
    assert r.status_code == 200


def test_geojson_territories():
    r = client.get("/api/v1/territories/geojson/all?type=commune")
    assert r.status_code == 200
    data = r.json()
    assert data["type"] == "FeatureCollection"


def test_layers():
    r = client.get("/api/v1/layers")
    assert r.status_code == 200
