import requests
import streamlit as st
from typing import Dict, Any, Optional, List, Union


def _base_url() -> str:
    """BASE_URL do Xano via st.secrets (OpenSpec RNF02)."""
    try:
        return st.secrets["xano"]["base_url"].rstrip("/")
    except Exception as e:
        raise RuntimeError(
            "Configure [xano].base_url em .streamlit/secrets.toml"
        ) from e


def _get_headers() -> Dict[str, str]:
    """Headers com Bearer token da sessão."""
    headers = {"Content-Type": "application/json"}
    if st.session_state.get("token"):
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return headers


def login(email: str, password: str) -> Dict[str, Any]:
    """POST /login → {access_token, user_id, name, email}."""
    response = requests.post(
        f"{_base_url()}/login",
        json={"email": email, "password": password},
        timeout=30,
    )
    data = response.json() if response.content else {}
    if not response.ok:
        raise Exception(data.get("message") or data.get("error") or f"Login failed ({response.status_code})")
    return data


def register(email: str, password: str, name: str) -> Dict[str, Any]:
    """POST /register."""
    response = requests.post(
        f"{_base_url()}/register",
        json={"email": email, "password": password, "name": name},
        timeout=30,
    )
    data = response.json() if response.content else {}
    if not response.ok:
        raise Exception(data.get("message") or data.get("error") or f"Register failed ({response.status_code})")
    return data


def api_get(endpoint: str) -> Optional[Union[Dict[str, Any], List[Any]]]:
    """GET autenticado."""
    try:
        with st.spinner("Carregando..."):
            response = requests.get(
                f"{_base_url()}{endpoint}",
                headers=_get_headers(),
                timeout=30,
            )
        if not response.ok:
            st.error(f"API error: {response.status_code} - {response.text}")
            return None
        return response.json() if response.content else {}
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return None


def api_post(endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """POST autenticado."""
    try:
        with st.spinner("Salvando..."):
            response = requests.post(
                f"{_base_url()}{endpoint}",
                json=data,
                headers=_get_headers(),
                timeout=30,
            )
        if not response.ok:
            st.error(f"API error: {response.status_code} - {response.text}")
            return None
        return response.json() if response.content else {}
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return None


def api_put(endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """PUT autenticado."""
    try:
        with st.spinner("Atualizando..."):
            response = requests.put(
                f"{_base_url()}{endpoint}",
                json=data,
                headers=_get_headers(),
                timeout=30,
            )
        if response.status_code == 204:
            return {}
        if not response.ok:
            st.error(f"API error: {response.status_code} - {response.text}")
            return None
        return response.json() if response.content else {}
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return None


def api_delete(endpoint: str) -> bool:
    """DELETE autenticado."""
    try:
        with st.spinner("Excluindo..."):
            response = requests.delete(
                f"{_base_url()}{endpoint}",
                headers=_get_headers(),
                timeout=30,
            )
        if response.status_code in (200, 204):
            return True
        st.error(f"API error: {response.status_code} - {response.text}")
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return False
