import pytest
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "DIGITAL FOSSIL"
    assert data["status"] == "ONLINE"

def test_login_success_and_roles():
    for role, email, password in [
        ("investigator", "investigator@digitalfossil.local", "investigator123"),
        ("reviewer", "reviewer@digitalfossil.local", "reviewer123"),
        ("admin", "admin@digitalfossil.local", "admin123")
    ]:
        resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
        assert resp.status_code == 200, f"Failed for {email}: {resp.text}"
        data = resp.json()
        assert "access_token" in data
        assert data["role"] == role

def test_login_invalid_credentials():
    resp = client.post("/api/v1/auth/login", json={"email": "admin@digitalfossil.local", "password": "wrongpassword"})
    assert resp.status_code == 401

def test_investigations_list_and_detail():
    login_resp = client.post("/api/v1/auth/login", json={"email": "investigator@digitalfossil.local", "password": "investigator123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    inv_list_resp = client.get("/api/v1/investigations", headers=headers)
    assert inv_list_resp.status_code == 200
    invs = inv_list_resp.json()
    assert len(invs) >= 1
    
    first_id = invs[0]["investigation_id"]
    detail_resp = client.get(f"/api/v1/investigations/{first_id}", headers=headers)
    assert detail_resp.status_code == 200
    detail = detail_resp.json()
    assert "observed_facts" in detail
    assert "inferences" in detail
    assert "hypotheses" in detail
    assert "graph" in detail

def test_reviewer_verdict_authorization():
    # Get available investigation ID
    admin_login = client.post("/api/v1/auth/login", json={"email": "admin@digitalfossil.local", "password": "admin123"})
    admin_token = admin_login.json()["access_token"]
    invs = client.get("/api/v1/investigations", headers={"Authorization": f"Bearer {admin_token}"}).json()
    target_id = invs[0]["investigation_id"]

    # Investigator cannot set reviewer verdict (403 forbidden)
    inv_login = client.post("/api/v1/auth/login", json={"email": "investigator@digitalfossil.local", "password": "investigator123"})
    inv_token = inv_login.json()["access_token"]

    resp = client.post(
        f"/api/v1/investigations/{target_id}/verdict",
        headers={"Authorization": f"Bearer {inv_token}"},
        json={"verdict": "approved", "comment": "Investigator trying to approve"}
    )
    assert resp.status_code == 403

    # Reviewer CAN set verdict
    rev_login = client.post("/api/v1/auth/login", json={"email": "reviewer@digitalfossil.local", "password": "reviewer123"})
    rev_token = rev_login.json()["access_token"]

    resp = client.post(
        f"/api/v1/investigations/{target_id}/verdict",
        headers={"Authorization": f"Bearer {rev_token}"},
        json={"verdict": "approved", "comment": "Verified evidence-backed sequence."}
    )
    assert resp.status_code == 200
    assert resp.json()["reviewer_verdict"] == "approved"

def test_report_pdf_export():
    login_resp = client.post("/api/v1/auth/login", json={"email": "investigator@digitalfossil.local", "password": "investigator123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    invs = client.get("/api/v1/investigations", headers=headers).json()
    target_id = invs[0]["investigation_id"]

    resp = client.get(f"/api/v1/reports/investigations/{target_id}/pdf", headers=headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert len(resp.content) > 1000

def test_collector_status():
    login_resp = client.post("/api/v1/auth/login", json={"email": "investigator@digitalfossil.local", "password": "investigator123"})
    token = login_resp.json()["access_token"]

    resp = client.get("/api/v1/collector/status", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert "privacy_notice" in data
    assert "is_running" in data
