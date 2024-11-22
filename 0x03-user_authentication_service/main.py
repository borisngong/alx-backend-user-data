import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    response = requests.post(
        f"{BASE_URL}/users",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200, f"Register failed: {response.text}"
    assert response.json() == {"email": email, "message": "user created"}, (
        "Unexpected response payload"
    )


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt login with the wrong password."""
    response = requests.post(
        f"{BASE_URL}/sessions",
        json={"email": email, "password": password}
    )
    assert response.status_code == 401, "Expected 401 for wrong password"


def log_in(email: str, password: str) -> str:
    """Log in and return session ID."""
    response = requests.post(
        f"{BASE_URL}/sessions",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    session_id = response.cookies.get("session_id")
    assert session_id, "No session ID returned"
    return session_id


def profile_unlogged() -> None:
    """Access profile while not logged in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, (
        "Expected 403 for unauthenticated profile access"
    )


def profile_logged(session_id: str) -> None:
    """Access profile while logged in."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, f"Profile access failed: {response.text}"
    assert "email" in response.json(), "Profile response missing email field"


def log_out(session_id: str) -> None:
    """Log out the user."""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, f"Logout failed: {response.text}"
    assert response.json() == {"message": "logout successful"}, (
        "Unexpected response payload"
    )


def reset_password_token(email: str) -> str:
    """Request a reset password token."""
    response = requests.post(
        f"{BASE_URL}/reset_password",
        json={"email": email}
    )
    assert response.status_code == 200, (
        f"Reset password token request failed: {response.text}"
    )
    reset_token = response.json().get("reset_token")
    assert reset_token, "No reset token returned"
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the user's password."""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        json={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    assert response.status_code == 200, (
        f"Update password failed: {response.text}"
    )
    assert response.json() == {"email": email, "message": "password updated"}, (
        "Unexpected response payload"
    )


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
