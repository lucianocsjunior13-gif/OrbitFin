import requests
import streamlit as st
from typing import Dict, Any, Optional

# Configuration
# In production, use st.secrets for these
# BASE_URL = st.secrets["xano"]["base_url"]
BASE_URL = "http://localhost:5000"  # Change to Xano API endpoint when deploying to Xano

def _get_headers() -> Dict[str, str]:
    """Get headers for API requests, including auth token if available."""
    headers = {}
    if "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return headers

def login(email: str, password: str) -> Dict[str, Any]:
    """Login to the backend and return token data."""
    try:
        response = requests.post(f"{BASE_URL}/api/login", json={"email": email, "password": password})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            return e.response.json()
        raise Exception(f"Connection error: {e}")

def register(email: str, password: str, name: str) -> Dict[str, Any]:
    """Register a new user."""
    try:
        response = requests.post(f"{BASE_URL}/api/register", json={"email": email, "password": password, "name": name})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            return e.response.json()
        raise Exception(f"Connection error: {e}")

def api_get(endpoint: str) -> Optional[Dict[str, Any]]:
    """Make a GET request to the backend."""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=_get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            st.error(f"API error: {e.response.status_code} - {e.response.text}")
        else:
            st.error(f"Connection error: {e}")
        return None

def api_post(endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Make a POST request to the backend."""
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=_get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            st.error(f"API error: {e.response.status_code} - {e.response.text}")
        else:
            st.error(f"Connection error: {e}")
        return None

def api_put(endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Make a PUT request to the backend."""
    try:
        response = requests.put(f"{BASE_URL}{endpoint}", json=data, headers=_get_headers())
        response.raise_for_status()
        if response.status_code == 204:
            return {}
        return response.json()
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            st.error(f"API error: {e.response.status_code} - {e.response.text}")
        else:
            st.error(f"Connection error: {e}")
        return None

def api_delete(endpoint: str) -> bool:
    """Make a DELETE request to the backend."""
    try:
        response = requests.delete(f"{BASE_URL}{endpoint}", headers=_get_headers())
        response.raise_for_status()
        return response.status_code in [200, 204]
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            st.error(f"API error: {e.response.status_code} - {e.response.text}")
        else:
            st.error(f"Connection error: {e}")
        return False