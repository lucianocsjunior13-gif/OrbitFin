import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'orbitfin.db')

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_database():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('receita', 'despesa')),
            valor REAL NOT NULL,
            data DATE NOT NULL,
            categoria TEXT,
            descricao TEXT,
            status TEXT NOT NULL CHECK(status IN ('pago', 'pendente')) DEFAULT 'pago',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Budgets table (limites por categoria)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT UNIQUE NOT NULL,
            limite REAL NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insights table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default budgets if none exist
    cursor.execute("SELECT COUNT(*) FROM budgets")
    if cursor.fetchone()[0] == 0:
        default_budgets = [
            ('Alimentação', 800.0),
            ('Moradia', 1200.0),
            ('Transporte', 400.0),
            ('Lazer', 300.0),
            ('Saúde', 200.0),
            ('Educação', 150.0),
            ('Outros', 500.0)
        ]
        cursor.executemany(
            "INSERT INTO budgets (categoria, limite) VALUES (?, ?)",
            default_budgets
        )
    
    # Insert default insight if none exists
    cursor.execute("SELECT COUNT(*) FROM insights")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO insights (texto) VALUES (?)",
            ("Comece registrando suas transações diárias para ter um melhor controle financeiro.",)
        )
    
    conn.commit()
    conn.close()

# Initialize database on module import
init_database()

# User management functions
def create_user(email: str, password: str, name: str) -> Dict[str, Any]:
    """Create a new user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (email, password, name) VALUES (?, ?, ?)",
            (email, password, name)
        )
        user_id = cursor.lastrowid
        conn.commit()
        
        # Return user data without password
        return {
            "id": user_id,
            "email": email,
            "name": name,
            "created_at": datetime.now().isoformat()
        }
    except sqlite3.IntegrityError:
        raise ValueError("Usuário com este e-mail já existe.")
    finally:
        conn.close()

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate a user and return user data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, email, name, created_at FROM users WHERE email = ? AND password = ?",
        (email, password)
    )
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

# Transaction management functions
def get_transactions(user_id: int) -> List[Dict]:
    """Get all transactions for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT id, tipo, valor, data, categoria, descricao, status, created_at
        FROM transactions
        WHERE user_id = ?
        ORDER BY data DESC, created_at DESC
        """,
        (user_id,)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def add_transaction(user_id: int, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a new transaction."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO transactions 
        (user_id, tipo, valor, data, categoria, descricao, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            transaction_data.get('tipo'),
            float(transaction_data.get('valor', 0)),
            transaction_data.get('data'),
            transaction_data.get('categoria', ''),
            transaction_data.get('descricao', ''),
            transaction_data.get('status', 'pago')
        )
    )
    
    transaction_id = cursor.lastrowid
    conn.commit()
    
    # Get the inserted transaction
    cursor.execute(
        """
        SELECT id, tipo, valor, data, categoria, descricao, status, created_at
        FROM transactions
        WHERE id = ?
        """,
        (transaction_id,)
    )
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else {}

def update_transaction(user_id: int, transaction_id: int, transaction_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update an existing transaction."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        UPDATE transactions
        SET tipo = ?,
            valor = ?,
            data = ?,
            categoria = ?,
            descricao = ?,
            status = ?
        WHERE id = ? AND user_id = ?
        """,
        (
            transaction_data.get('tipo'),
            float(transaction_data.get('valor', 0)),
            transaction_data.get('data'),
            transaction_data.get('categoria', ''),
            transaction_data.get('descricao', ''),
            transaction_data.get('status', 'pago'),
            transaction_id,
            user_id
        )
    )
    
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return None
    
    # Get the updated transaction
    cursor.execute(
        """
        SELECT id, tipo, valor, data, categoria, descricao, status, created_at
        FROM transactions
        WHERE id = ?
        """,
        (transaction_id,)
    )
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else {}

def delete_transaction(user_id: int, transaction_id: int) -> bool:
    """Delete a transaction."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM transactions WHERE id = ? AND user_id = ?",
        (transaction_id, user_id)
    )
    
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    
    return deleted

# Budget management functions
def get_budgets() -> List[Dict]:
    """Get all budget definitions."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, categoria, limite, updated_at FROM budgets ORDER BY categoria"
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def update_budget(budget_id: int, limite: float) -> Optional[Dict[str, Any]]:
    """Update a budget limit."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE budgets SET limite = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (limite, budget_id)
    )
    
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return None
    
    # Get the updated budget
    cursor.execute(
        "SELECT id, categoria, limite, updated_at FROM budgets WHERE id = ?",
        (budget_id,)
    )
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else {}

# Insights functions
def get_insights() -> Dict[str, Any]:
    """Get insights data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, texto, updated_at FROM insights ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else {}

def update_insights(texto: str) -> Dict[str, Any]:
    """Update insights text."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE insights SET texto = ?, updated_at = CURRENT_TIMESTAMP WHERE id = (SELECT id FROM insights ORDER BY id DESC LIMIT 1)"
    )
    
    if cursor.rowcount == 0:
        # No insights exist, insert one
        cursor.execute(
            "INSERT INTO insights (texto) VALUES (?)",
            (texto,)
        )
    
    conn.commit()
    
    # Get the updated insight
    cursor.execute(
        "SELECT id, texto, updated_at FROM insights ORDER BY id DESC LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else {}

# Helper function to calculate expenses by category
def get_expenses_by_category(user_id: int) -> Dict[str, float]:
    """Calculate total expenses by category for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT categoria, SUM(valor) as total
        FROM transactions
        WHERE user_id = ? AND tipo = 'despesa'
        GROUP BY categoria
        """,
        (user_id,)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    return {row['categoria']: float(row['total']) for row in rows if row['categoria']}

# Helper function to calculate income by category
def get_income_by_category(user_id: int) -> Dict[str, float]:
    """Calculate total income by category for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT categoria, SUM(valor) as total
        FROM transactions
        WHERE user_id = ? AND tipo = 'receita'
        GROUP BY categoria
        """,
        (user_id,)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    return {row['categoria']: float(row['total']) for row in rows if row['categoria']}

# Reporting functions for the Relatórios page
def get_monthly_summary(user_id: int, year: int = None, month: int = None) -> Dict[str, Any]:
    """Get monthly summary of income vs expenses."""
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get total income and expenses for the month
    cursor.execute(
        """
        SELECT 
            SUM(CASE WHEN tipo = 'receita' THEN valor ELSE 0 END) as total_receitas,
            SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END) as total_despesas
        FROM transactions
        WHERE user_id = ? 
        AND strftime('%Y', data) = ? 
        AND strftime('%m', data) = ?
        """,
        (user_id, str(year), f"{month:02d}")
    )
    
    row = cursor.fetchone()
    total_receitas = float(row['total_receitas']) if row['total_receitas'] else 0.0
    total_despesas = float(row['total_despesas']) if row['total_despesas'] else 0.0
    
    # Get expenses by category for the month
    cursor.execute(
        """
        SELECT categoria, SUM(valor) as total
        FROM transactions
        WHERE user_id = ? AND tipo = 'despesa'
        AND strftime('%Y', data) = ? 
        AND strftime('%m', data) = ?
        GROUP BY categoria
        ORDER BY total DESC
        """,
        (user_id, str(year), f"{month:02d}")
    )
    
    expenses_by_category = [
        {'categoria': row['categoria'], 'total': float(row['total'])}
        for row in cursor.fetchall()
    ]
    
    # Get income by category for the month
    cursor.execute(
        """
        SELECT categoria, SUM(valor) as total
        FROM transactions
        WHERE user_id = ? AND tipo = 'receita'
        AND strftime('%Y', data) = ? 
        AND strftime('%m', data) = ?
        GROUP BY categoria
        ORDER BY total DESC
        """,
        (user_id, str(year), f"{month:02d}")
    )
    
    income_by_category = [
        {'categoria': row['categoria'], 'total': float(row['total'])}
        for row in cursor.fetchall()
    ]
    
    conn.close()
    
    return {
        'year': year,
        'month': month,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'balance': total_receitas - total_despesas,
        'expenses_by_category': expenses_by_category,
        'income_by_category': income_by_category
    }

def get_yearly_summary(user_id: int, year: int = None) -> Dict[str, Any]:
    """Get yearly summary of income vs expenses."""
    if year is None:
        year = datetime.now().year
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get total income and expenses for the year
    cursor.execute(
        """
        SELECT 
            SUM(CASE WHEN tipo = 'receita' THEN valor ELSE 0 END) as total_receitas,
            SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END) as total_despesas
        FROM transactions
        WHERE user_id = ? 
        AND strftime('%Y', data) = ?
        """,
        (user_id, str(year))
    )
    
    row = cursor.fetchone()
    total_receitas = float(row['total_receitas']) if row['total_receitas'] else 0.0
    total_despesas = float(row['total_despesas']) if row['total_despesas'] else 0.0
    
    # Get monthly breakdown
    cursor.execute(
        """
        SELECT 
            strftime('%m', data) as month,
            SUM(CASE WHEN tipo = 'receita' THEN valor ELSE 0 END) as receitas,
            SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END) as despesas
        FROM transactions
        WHERE user_id = ? AND strftime('%Y', data) = ?
        GROUP BY strftime('%m', data)
        ORDER BY month
        """,
        (user_id, str(year))
    )
    
    monthly_data = []
    for row in cursor.fetchall():
        monthly_data.append({
            'month': int(row['month']),
            'receitas': float(row['receitas']) if row['receitas'] else 0.0,
            'despesas': float(row['despesas']) if row['despesas'] else 0.0,
            'balance': float(row['receitas']) - float(row['despesas'])
        })
    
    conn.close()
    
    return {
        'year': year,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'balance': total_receitas - total_despesas,
        'monthly_data': monthly_data
    }