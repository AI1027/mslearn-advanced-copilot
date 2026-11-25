from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_countries():
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]


def test_regions_spain() -> None:
    """Return the exact city list for Spain."""
    response = client.get("/regions/Spain")
    assert response.status_code == 200
    assert response.json() == ["Seville"]


def test_unknown_region() -> None:
    """Return the agreed 404 detail for an unknown region."""
    response = client.get("/regions/Atlantis")
    assert response.status_code == 404
    assert response.json() == {"detail": "Region not found"}


def test_post_regions_not_allowed() -> None:
    """Reject POST requests to the GET-only city-list route."""
    response = client.post("/regions/Spain")
    assert response.status_code == 405


def test_regions_route_is_in_openapi() -> None:
    """Expose the region city-list route in the generated schema."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/regions/{region}" in response.json()["paths"]


def test_monthly_weather_routes() -> None:
    """Preserve both monthly weather route paths and their response."""
    region_response = client.get("/regions/Spain/Seville/January")
    assert region_response.status_code == 200
    assert region_response.json() == {"high": 61, "low": 41}

    countries_response = client.get("/countries/Spain/Seville/January")
    assert countries_response.status_code == 200
    assert countries_response.json() == {"high": 61, "low": 41}