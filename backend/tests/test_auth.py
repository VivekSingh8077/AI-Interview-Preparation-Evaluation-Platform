def test_register_creates_user_and_returns_token(client):
    resp = client.post(
        "/api/auth/register",
        json={"name": "Ada Lovelace", "email": "ada@example.com", "password": "supersecret1"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["access_token"]
    assert body["user"]["email"] == "ada@example.com"
    assert "password" not in body["user"]


def test_register_duplicate_email_rejected(client):
    payload = {"name": "Ada", "email": "dup@example.com", "password": "supersecret1"}
    client.post("/api/auth/register", json=payload)
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 409


def test_login_success(client):
    client.post(
        "/api/auth/register",
        json={"name": "Grace Hopper", "email": "grace@example.com", "password": "supersecret1"},
    )
    resp = client.post(
        "/api/auth/login", json={"email": "grace@example.com", "password": "supersecret1"}
    )
    assert resp.status_code == 200
    assert resp.json()["access_token"]


def test_login_wrong_password_rejected(client):
    client.post(
        "/api/auth/register",
        json={"name": "Grace Hopper", "email": "grace2@example.com", "password": "supersecret1"},
    )
    resp = client.post(
        "/api/auth/login", json={"email": "grace2@example.com", "password": "wrongpass"}
    )
    assert resp.status_code == 401


def test_protected_route_requires_token(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_protected_route_with_valid_token(client):
    register_resp = client.post(
        "/api/auth/register",
        json={"name": "Alan Turing", "email": "alan@example.com", "password": "supersecret1"},
    )
    token = register_resp.json()["access_token"]

    resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "alan@example.com"


def test_health_check(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
