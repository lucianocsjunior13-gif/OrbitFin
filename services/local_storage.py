import json
import os
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any

# Data directory path
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# File paths for different data types
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
TRANSACTIONS_FILE = os.path.join(DATA_DIR, 'transactions.json')
BUDGETS_FILE = os.path.join(DATA_DIR, 'budgets.json')
INSIGHTS_FILE = os.path.join(DATA_DIR, 'insights.json')

def _load_data(filepath: str) -> List[Dict]:
    """Load data from a JSON file."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def _save_data(filepath: str, data: List[Dict]) -> None:
    """Save data to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def _get_next_id(items: List[Dict]) -> int:
    """Get the next available ID for a new item."""
    if not items:
        return 1
    return max(item.get('id', 0) for item in items) + 1

# User management functions
def create_user(email: str, password: str, name: str) -> Dict[str, Any]:
    """Create a new user."""
    users = _load_data(USERS_FILE)
    
    # Check if user already exists
    if any(user.get('email') == email for user in users):
        raise ValueError("Usuário com este e-mail já existe.")
    
    user = {
        "id": _get_next_id(users),
        "email": email,
        "password": password,  # In a real app, this should be hashed
        "name": name,
        "created_at": datetime.now().isoformat()
    }
    
    users.append(user)
    _save_data(USERS_FILE, users)
    
    # Return user data without password
    return {k: v for k, v in user.items() if k != 'password'}

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate a user and return user data."""
    users = _load_data(USERS_FILE)
    
    for user in users:
        if user.get('email') == email and user.get('password') == password:
            # Return user data without password
            return {k: v for k, v in user.items() if k != 'password'}
    
    return None

# Transaction management functions
def get_transactions(user_id: int) -> List[Dict]:
    """Get all transactions for a user."""
    transactions = _load_data(TRANSACTIONS_FILE)
    return [t for t in transactions if t.get('user_id') == user_id]

def add_transaction(user_id: int, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a new transaction."""
    transactions = _load_data(TRANSACTIONS_FILE)
    
    transaction = {
        "id": _get_next_id(transactions),
        "user_id": user_id,
        "tipo": transaction_data.get('tipo'),
        "valor": float(transaction_data.get('valor', 0)),
        "data": transaction_data.get('data'),
        "categoria": transaction_data.get('categoria', ''),
        "descricao": transaction_data.get('descricao', ''),
        "status": transaction_data.get('status', 'pago'),
        "created_at": datetime.now().isoformat()
    }
    
    transactions.append(transaction)
    _save_data(TRANSACTIONS_FILE, transactions)
    return transaction

def update_transaction(user_id: int, transaction_id: int, transaction_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update an existing transaction."""
    transactions = _load_data(TRANSACTIONS_FILE)
    
    for i, transaction in enumerate(transactions):
        if transaction.get('id') == transaction_id and transaction.get('user_id') == user_id:
            # Update transaction fields
            transactions[i].update({
                "tipo": transaction_data.get('tipo', transactions[i].get('tipo')),
                "valor": float(transaction_data.get('valor', transactions[i].get('valor', 0))),
                "data": transaction_data.get('data', transactions[i].get('data')),
                "categoria": transaction_data.get('categoria', transactions[i].get('categoria', '')),
                "descricao": transaction_data.get('descricao', transactions[i].get('descricao', '')),
                "status": transaction_data.get('status', transactions[i].get('status', 'pago')),
                "updated_at": datetime.now().isoformat()
            })
            
            _save_data(TRANSACTIONS_FILE, transactions)
            return transactions[i]
    
    return None

def delete_transaction(user_id: int, transaction_id: int) -> bool:
    """Delete a transaction."""
    transactions = _load_data(TRANSACTIONS_FILE)
    
    for i, transaction in enumerate(transactions):
        if transaction.get('id') == transaction_id and transaction.get('user_id') == user_id:
            del transactions[i]
            _save_data(TRANSACTIONS_FILE, transactions)
            return True
    
    return False

# Budget management functions
def get_budgets() -> List[Dict]:
    """Get all budget definitions."""
    budgets = _load_data(BUDGETS_FILE)
    
    # If no budgets exist, create default ones
    if not budgets:
        default_budgets = [
            {
                "id": 1,
                "categoria": "Alimentação",
                "limite": 800.0
            },
            {
                "id": 2,
                "categoria": "Moradia",
                "limite": 1200.0
            },
            {
                "id": 3,
                "categoria": "Transporte",
                "limite": 400.0
            },
            {
                "id": 4,
                "categoria": "Lazer",
                "limite": 300.0
            },
            {
                "id": 5,
                "categoria": "Saúde",
                "limite": 200.0
            },
            {
                "id": 6,
                "categoria": "Educação",
                "limite": 150.0
            }
        ]
        _save_data(BUDGETS_FILE, default_budgets)
        return default_budgets
    
    return budgets

def update_budget(budget_id: int, limite: float) -> Optional[Dict[str, Any]]:
    """Update a budget limit."""
    budgets = _load_data(BUDGETS_FILE)
    
    for i, budget in enumerate(budgets):
        if budget.get('id') == budget_id:
            budgets[i]["limite"] = float(limite)
            budgets[i]["updated_at"] = datetime.now().isoformat()
            _save_data(BUDGETS_FILE, budgets)
            return budgets[i]
    
    return None

# Insights functions
def get_insights() -> Dict[str, Any]:
    """Get insights data."""
    insights_data = _load_data(INSIGHTS_FILE)
    
    # If no insights exist, create default one
    if not insights_data:
        default_insight = {
            "id": 1,
            "texto": "Comece registrando suas transações diárias para ter um melhor controle financeiro.",
            "created_at": datetime.now().isoformat()
        }
        _save_data(INSIGHTS_FILE, [default_insight])
        return default_insight
    
    return insights_data[0] if insights_data else {}

def update_insights(texto: str) -> Dict[str, Any]:
    """Update insights text."""
    insights_data = _load_data(INSIGHTS_FILE)
    
    if insights_data:
        insights_data[0]["texto"] = texto
        insights_data[0]["updated_at"] = datetime.now().isoformat()
    else:
        insights_data = [{
            "id": 1,
            "texto": texto,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }]
    
    _save_data(INSIGHTS_FILE, insights_data)
    return insights_data[0]

# Helper function to calculate expenses by category
def get_expenses_by_category(user_id: int) -> Dict[str, float]:
    """Calculate total expenses by category for a user."""
    transactions = get_transactions(user_id)
    expenses_by_category = {}
    
    for transaction in transactions:
        if transaction.get('tipo') == 'despesa':
            categoria = transaction.get('categoria', 'Outros')
            valor = float(transaction.get('valor', 0))
            expenses_by_category[categoria] = expenses_by_category.get(categoria, 0) + valor
    
    return expenses_by_category

# Helper function to calculate income by category
def get_income_by_category(user_id: int) -> Dict[str, float]:
    """Calculate total income by category for a user."""
    transactions = get_transactions(user_id)
    income_by_category = {}
    
    for transaction in transactions:
        if transaction.get('tipo') == 'receita':
            categoria = transaction.get('categoria', 'Outros')
            valor = float(transaction.get('valor', 0))
            income_by_category[categoria] = income_by_category.get(categoria, 0) + valor
    
    return income_by_category