def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_redirect_and_analytics(client):
    response = client.post("/api/v1/urls", json={"original_url": "https://example.com/docs"})
    assert response.status_code == 201
    body = response.json()
    code = body["short_code"]
    assert body["original_url"] == "https://example.com/docs"

    redirect = client.get(f"/{code}", follow_redirects=False)
    assert redirect.status_code == 307
    assert redirect.headers["location"] == "https://example.com/docs"

    analytics = client.get(f"/api/v1/urls/{code}/analytics")
    assert analytics.status_code == 200
    assert analytics.json()["click_count"] == 1


def test_missing_code_returns_404(client):
    assert client.get("/does-not-exist").status_code == 404
    assert client.get("/api/v1/urls/nope/analytics").status_code == 404


def test_invalid_url_returns_422(client):
    response = client.post("/api/v1/urls", json={"original_url": "not-a-url"})
    assert response.status_code == 422
