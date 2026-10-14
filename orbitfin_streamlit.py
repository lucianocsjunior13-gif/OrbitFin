import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px

# Configuration
# In production, use st.secrets for these
# BASE_URL = st.secrets["xano"]["base_url"]
BASE_URL = "http://localhost:5000"  # Change to Xano API endpoint when deploying to Xano

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'transacoes' not in st.session_state:
    st.session_state.transacoes = []  # Cache for transactions

def login(email, password):
    """Login to the backend and store token."""
    try:
        with st.spinner("Logging in..."):
            response = requests.post(f"{BASE_URL}/api/login", json={"email": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data.get("access_token")
            st.session_state.logged_in = True
            st.session_state.user = email
            return True, "Login successful"
        else:
            return False, response.json().get("error", "Login failed")
    except Exception as e:
        return False, f"Connection error: {e}"

def register(email, password, name):
    """Register a new user."""
    try:
        with st.spinner("Registering..."):
            response = requests.post(f"{BASE_URL}/api/register", json={"email": email, "password": password, "name": name})
        if response.status_code in [200, 201]:
            return True, "Registration successful. Please log in."
        else:
            return False, response.json().get("error", "Registration failed")
    except Exception as e:
        return False, f"Connection error: {e}"

def logout():
    """Logout user."""
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.transacoes = []

def api_get(endpoint):
    """Make a GET request to the backend."""
    headers = {}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    try:
        with st.spinner("Loading..."):
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def api_post(endpoint, data):
    """Make a POST request to the backend."""
    headers = {}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    try:
        with st.spinner("Saving..."):
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def api_put(endpoint, data):
    """Make a PUT request to the backend."""
    headers = {}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    try:
        with st.spinner("Updating..."):
            response = requests.put(f"{BASE_URL}{endpoint}", json=data, headers=headers)
        if response.status_code in [200, 204]:
            return response.json() if response.status_code == 200 else {}
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def api_delete(endpoint):
    """Make a DELETE request to the backend."""
    headers = {}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    try:
        with st.spinner("Deleting..."):
            response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
        if response.status_code in [200, 204]:
            return True
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Connection error: {e}")
        return False

def main():
    st.set_page_config(page_title="OrbitFin", page_icon="💰", layout="wide")
    
    # Sidebar for login/logout and registration
    with st.sidebar:
        if st.session_state.logged_in:
            st.write(f"Logged in as: {st.session_state.user}")
            if st.button("Logout"):
                logout()
                st.experimental_rerun()
        else:
            st.subheader("Login")
            email = st.text_input("Email", value="admin@orbitfin.com", key="login_email")
            password = st.text_input("Password", type="password", value="OrbitFin2026", key="login_password")
            if st.button("Login"):
                success, message = login(email, password)
                if success:
                    st.success(message)
                    st.experimental_rerun()
                else:
                    st.error(message)
            
            st.divider()
            st.subheader("Register")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_name = st.text_input("Full Name", key="reg_name")
            if st.button("Register"):
                success, message = register(reg_email, reg_password, reg_name)
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    # Main app
    if not st.session_state.logged_in:
        st.warning("Please log in to access the application.")
        return
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Transações", "Orçamento", "Metas"])
    
    # Dashboard Tab
    with tab1:
        st.header("Dashboard Financeiro")
        
        # Fetch data
        saldo_data = api_get("/api/saldo")
        transacoes_data = api_get("/api/transacoes")
        insights_data = api_get("/api/insights")
        budgets_data = api_get("/api/budgets")
        
        # Cache transactions for use in other tabs
        if transacoes_data:
            st.session_state.transacoes = transacoes_data
        
        # Display KPIs
        col1, col2, col3 = st.columns(3)
        with col1:
            saldo_val = saldo_data.get("valor", 0) if saldo_data else 0
            st.metric("Saldo Atual", f"R$ {saldo_val:,.2f}")
        with col2:
            # Calculate total expenses (assuming transacoes has a 'tipo' field: 'despesa' or 'receita')
            total_despesas = 0
            if transacoes_data:
                for t in transacoes_data:
                    if t.get('tipo') == 'despesa':
                        total_despesas += t.get('valor', 0)
            st.metric("Total Gasto (Mês)", f"R$ {total_despesas:,.2f}")
        with col3:
            total_receitas = 0
            if transacoes_data:
                for t in transacoes_data:
                    if t.get('tipo') == 'receita':
                        total_receitas += t.get('valor', 0)
            st.metric("Total Receitas (Mês)", f"R$ {total_receitas:,.2f}")
        
        # Chart: Receitas vs Despesas Mensais
        st.subheader("Receitas vs Despesas Mensais")
        if transacoes_data:
            # Prepare data for chart
            df = pd.DataFrame(transacoes_data)
            if not df.empty and 'data' in df.columns and 'tipo' in df.columns and 'valor' in df.columns:
                # Convert data to datetime
                df['data'] = pd.to_datetime(df['data'])
                df['mês'] = df['data'].dt.to_period('M')
                # Group by mês and tipo
                chart_data = df.groupby(['mês', 'tipo'])['valor'].sum().reset_index()
                chart_data['mês_str'] = chart_data['mês'].astype(str)
                fig = px.bar(chart_data, x='mês_str', y='valor', color='tipo', 
                             title="Receitas vs Despesas por Mês",
                             labels={'mês_str': 'Mês', 'valor': 'Valor (R$)', 'tipo': 'Tipo'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Não há dados suficientes para exibir o gráfico.")
        else:
            st.info("Nenhuma transação encontrada.")
        
        # Insights
        st.subheader("Insights")
        if insights_data and isinstance(insights_data, dict) and 'texto' in insights_data:
            st.write(insights_data['texto'])
        else:
            st.write("Nenhum insight disponível.")
    
    # Transações Tab
    with tab2:
        st.header("Gestão de Transações")
        
        # Form to add new transaction
        with st.expander("Adicionar Nova Transação"):
            with st.form("nova_transacao"):
                tipo = st.selectbox("Tipo", ["receita", "despesa"])
                valor = st.number_input("Valor", min_value=0.01, step=0.01)
                data = st.date_input("Data", value=datetime.now())
                categoria = st.text_input("Categoria", value="")
                descricao = st.text_input("Descrição")
                status = st.selectbox("Status", ["pago", "pendente"])
                submitted = st.form_submit_button("Adicionar")
                if submitted:
                    # Prepare data
                    transacao_data = {
                        "tipo": tipo,
                        "valor": valor,
                        "data": data.strftime("%Y-%m-%d"),
                        "categoria": categoria,
                        "descricao": descricao,
                        "status": status
                    }
                    result = api_post("/api/transacoes", transacao_data)
                    if result:
                        st.success("Transação adicionada com sucesso!")
                        # Refresh transactions list
                        st.session_state.transacoes = api_get("/api/transacoes") or []
                        st.experimental_rerun()
                    else:
                        st.error("Falha ao adicionar transação.")
        
        # Display transactions with edit/delete
        st.subheader("Lista de Transações")
        transacoes_data = st.session_state.transacoes or api_get("/api/transacoes") or []
        if transacoes_data:
            df = pd.DataFrame(transacoes_data)
            if not df.empty:
                # Allow filtering
                col1, col2, col3 = st.columns(3)
                with col1:
                    tipo_filter = st.selectbox("Filtrar por Tipo", ["Todos", "receita", "despesa"])
                with col2:
                    status_filter = st.selectbox("Filtrar por Status", ["Todos", "pago", "pendente"])
                with col3:
                    # Category filter - get unique categories
                    categorias = ["Todas"] + list(df['categoria'].unique()) if 'categoria' in df.columns else ["Todas"]
                    categoria_filter = st.selectbox("Filtrar por Categoria", categorias)
                
                # Apply filters
                filtered_df = df.copy()
                if tipo_filter != "Todos":
                    filtered_df = filtered_df[filtered_df['tipo'] == tipo_filter]
                if status_filter != "Todos":
                    filtered_df = filtered_df[filtered_df['status'] == status_filter]
                if categoria_filter != "Todas":
                    filtered_df = filtered_df[filtered_df['categoria'] == categoria_filter]
                
                # Display table with edit/delete buttons
                for idx, row in filtered_df.iterrows():
                    with st.container():
                        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
                        with col1:
                            st.write(f"**{row.get('tipo', '').title()}**: {row.get('descricao', 'Sem descrição')}")
                            st.write(f"R$ {row.get('valor', 0):,.2f} • {row.get('data', 'Data não informada')} • {row.get('categoria', 'Sem categoria')} • {row.get('status', 'Status não informado')}")
                        with col2:
                            if st.button("Editar", key=f"edit_{idx}"):
                                st.session_state[f"editing_{idx}"] = True
                                st.experimental_rerun()
                        with col3:
                            if st.button("Excluir", key=f"delete_{idx}"):
                                # Assuming we have an endpoint to delete by ID
                                # We need the transaction ID, which we assume is in the row as 'id'
                                transacao_id = row.get('id')
                                if transacao_id and api_delete(f"/api/transacoes/{transacao_id}"):
                                    st.success("Transação excluída!")
                                    # Refresh transactions list
                                    st.session_state.transacoes = api_get("/api/transacoes") or []
                                    st.experimental_rerun()
                                else:
                                    st.error("Falha ao excluir transação.")
                        # Edit form
                        if st.session_state.get(f"editing_{idx}", False):
                            with st.form(f"edit_form_{idx}"):
                                edit_tipo = st.selectbox("Tipo", ["receita", "despesa"], index=0 if row.get('tipo') == 'receita' else 1)
                                edit_valor = st.number_input("Valor", min_value=0.01, step=0.01, value=float(row.get('valor', 0)))
                                edit_data = st.date_input("Data", value=pd.to_datetime(row.get('data')) if row.get('data') else datetime.now())
                                edit_categoria = st.text_input("Categoria", value=row.get('categoria', ''))
                                edit_descricao = st.text_input("Descrição", value=row.get('descricao', ''))
                                edit_status = st.selectbox("Status", ["pago", "pendente"], index=0 if row.get('status') == 'pago' else 1)
                                submit_edit = st.form_submit_button("Salvar Alterações")
                                if submit_edit:
                                    update_data = {
                                        "tipo": edit_tipo,
                                        "valor": edit_valor,
                                        "data": edit_data.strftime("%Y-%m-%d"),
                                        "categoria": edit_categoria,
                                        "descricao": edit_descricao,
                                        "status": edit_status
                                    }
                                    transacao_id = row.get('id')
                                    if transacao_id and api_put(f"/api/transacoes/{transacao_id}", update_data):
                                        st.success("Transação atualizada!")
                                        st.session_state[f"editing_{idx}"] = False
                                        # Refresh transactions list
                                        st.session_state.transacoes = api_get("/api/transacoes") or []
                                        st.experimental_rerun()
                                    else:
                                        st.error("Falha ao atualizar transação.")
                                cancel_edit = st.form_submit_button("Cancelar")
                                if cancel_edit:
                                    st.session_state[f"editing_{idx}"] = False
                                    st.experimental_rerun()
                        st.divider()
            else:
                st.info("Nenhuma transação encontrada.")
        else:
            st.info("Não foi possível carregar as transações.")
    
    # Orçamento Tab
    with tab3:
        st.header("Orçamento e Categorias")
        
        budgets_data = api_get("/api/budgets")
        if budgets_data:
            st.subheader("Limites por Categoria")
            for budget in budgets_data:
                categoria = budget.get('categoria', 'N/A')
                gasto_atual = budget.get('gastoAtual', 0.0)
                limite = budget.get('limite', 0.0)
                percentual = budget.get('percentual', 0)
                
                st.write(f"**{categoria}**")
                progress = min(gasto_atual / limite, 1.0) if limite > 0 else 0
                st.progress(progress)
                st.write(f"Gasto: R$ {gasto_atual:,.2f} / Limite: R$ {limite:,.2f} ({percentual}%)")
                if gasto_atual > limite:
                    st.error("⚠️ Limite ultrapassado!")
                else:
                    st.success("Dentro do limite")
                st.divider()
        else:
            st.info("Não foi possível carregar os dados de orçamento.")
        
        # Allow editing budget limits (if backend supports it)
        # For now, we just display
    
    # Metas Tab
    with tab4:
        st.header("Metas de Economia")
        
        # We can use the budgets data to show progress towards goals
        budgets_data = api_get("/api/budgets")
        if budgets_data:
            st.subheader("Progresso das Metas")
            for budget in budgets_data:
                categoria = budget.get('categoria', 'N/A')
                gasto_atual = budget.get('gastoAtual', 0.0)
                limite = budget.get('limite', 0.0)
                restante = limite - gasto_atual
                
                st.write(f"**Meta para {categoria}**")
                if limite > 0:
                    percentual_usado = (gasto_atual / limite) * 100
                    st.progress(min(gasto_atual / limite, 1.0))
                    st.write(f"Gasto: R$ {gasto_atual:,.2f} de R$ {limite:,.2f}")
                    st.write(f"Restante: R$ {restante:,.2f}")
                    if restante <= 0:
                        st.error("Meta atingida ou ultrapassada!")
                    else:
                        st.info(f"Faltam R$ {restante:,.2f} para atingir a meta.")
                else:
                    st.write("Meta não definida (limite não informado).")
                st.divider()
        else:
            st.info("Não foi possível carregar os dados de metas.")

if __name__ == "__main__":
    main()