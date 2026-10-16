import streamlit as st
from services.storage import (
    get_budgets, update_budget,
    get_expenses_by_category, get_income_by_category
)
import pandas as pd
from datetime import datetime
import plotly.express as px

from components.theme import page_config, apply_theme
from components.sidebar import render_sidebar
from components.header import render_header
from views.login import render_login
from views.register import render_register
from views.dashboard import render_dashboard
from views.transactions import render_transactions

page_config()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'token' not in st.session_state:
    st.session_state.token = None
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"
if 'auth_page' not in st.session_state:
    st.session_state.auth_page = "login"

def main_app():
    """Main application after login."""
    apply_theme(hide_sidebar=False, auth=False)
    render_sidebar()

    if st.session_state.page == "dashboard":
        render_dashboard()
    elif st.session_state.page == "transacoes":
        render_header("transacoes")
        render_transactions()
    elif st.session_state.page == "orcamento":
        render_header("orcamento")
        show_budget()
    elif st.session_state.page == "metas":
        render_header("metas")
        show_goals()
    elif st.session_state.page == "relatorios":
        render_header("relatorios")
        show_relatorios()

def show_budget():
    """Display the budget page."""
    user_id = st.session_state.user['id']
    
    # Get data
    budgets = get_budgets()
    expenses_by_category = get_expenses_by_category(user_id)
    
    st.subheader("📊 Limites por Categoria")
    
    for budget in budgets:
        categoria = budget.get('categoria', 'N/A')
        limite = float(budget.get('limite', 0))
        gasto_atual = float(expenses_by_category.get(categoria, 0))
        percentual = (gasto_atual / limite * 100) if limite > 0 else 0
        
        st.write(f"**{categoria}**")
        
        # Progress bar
        progress = min(gasto_atual / limite, 1.0) if limite > 0 else 0
        st.progress(progress)
        
        # Details
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"Gasto: R$ {gasto_atual:,.2f}")
        with col2:
            st.write(f"Limite: R$ {limite:,.2f}")
        with col3:
            st.write(f"{percentual:.1f}%")
        
        # Status indicator
        if gasto_atual > limite:
            st.error("⚠️ Limite ultrapassado!")
        elif gasto_atual == limite:
            st.warning("⚠️ Limite atingido")
        else:
            restante = limite - gasto_atual
            st.success(f"✅ Dentro do limite (R$ {restante:,.2f} disponível)")
        
        st.divider()
    
    # Allow editing budget limits (optional feature)
    with st.expander("⚙️ Ajustar Limites de Orçamento"):
        st.info("Ajuste os limites de gastos por categoria conforme sua necessidade.")
        
        for budget in budgets:
            categoria = budget.get('categoria', 'N/A')
            limite_atual = float(budget.get('limite', 0))
            
            novo_limite = st.number_input(
                f"Limite para {categoria} (R$)",
                min_value=0.0,
                step=50.0,
                value=limite_atual,
                format="%.2f",
                key=f"budget_{budget['id']}"
            )
            
            if st.button(f"Atualizar {categoria}", key=f"update_budget_{budget['id']}"):
                if update_budget(budget['id'], novo_limite):
                    st.success(f"Limite para {categoria} atualizado para R$ {novo_limite:,.2f}")
                    st.rerun()
                else:
                    st.error(f"Erro ao atualizar limite para {categoria}")

def show_goals():
    """Display the goals/savings page."""
    user_id = st.session_state.user['id']
    
    # Get data
    budgets = get_budgets()
    expenses_by_category = get_expenses_by_category(user_id)
    
    st.subheader("🎯 Progresso das Metas")
    
    for budget in budgets:
        categoria = budget.get('categoria', 'N/A')
        limite = float(budget.get('limite', 0))
        gasto_atual = float(expenses_by_category.get(categoria, 0))
        restante = limite - gasto_atual
        
        st.write(f"**Meta para {categoria}**")
        
        if limite > 0:
            percentual_usado = (gasto_atual / limite) * 100
            progress = min(gasto_atual / limite, 1.0)
            
            st.progress(progress)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"Gasto: R$ {gasto_atual:,.2f}")
            with col2:
                st.write(f"Limite: R$ {limite:,.2f}")
            with col3:
                st.write(f"Restante: R$ {restante:,.2f}")
            
            # Status indicators
            if restante <= 0:
                st.error("🎉 Meta atingida ou ultrapassada!")
            elif restante <= limite * 0.1:  # Less than 10% remaining
                st.warning("⚠️ Quase atingindo o limite")
            else:
                st.info(f"✅ Faltam R$ {restante:,.2f} para atingir a meta")
        else:
            st.write("Meta não definida (limite não informado)")
        
        st.divider()

def show_relatorios():
    import streamlit as st
    import pandas as pd
    from datetime import datetime
    import plotly.express as px
    import plotly.graph_objects as go
    from services.storage import (
        get_transactions,
        get_expenses_by_category,
        get_income_by_category,
        get_monthly_summary,
        get_yearly_summary
    )

    # Initialize session state for user if not present (should be set by main app, but just in case)
    if 'user' not in st.session_state or not st.session_state.user:
        st.warning("Please log in to access the application.")
        return

    user_id = st.session_state.user['id']
    
    # Date selectors
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox(
            "Ano",
            options=list(range(datetime.now().year - 5, datetime.now().year + 1)),
            index=5  # Current year
        )
    with col2:
        month = st.selectbox(
            "Mês",
            options=list(range(1, 13)),
            format_func=lambda x: datetime(2000, x, 1).strftime('%B'),
            index=datetime.now().month - 1
        )
    
    st.divider()
    
    # Monthly Summary
    st.subheader(f"📅 Resumo de {datetime(2000, month, 1).strftime('%B')} de {year}")
    
    monthly_data = get_monthly_summary(user_id, year, month)
    
    # KPIs for the month
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Receitas",
            value=f"R$ {monthly_data['total_receitas']:,.2f}"
        )
    with col2:
        st.metric(
            label="Total Despesas",
            value=f"R$ {monthly_data['total_despesas']:,.2f}"
        )
    with col3:
        st.metric(
            label="Saldo do Mês",
            value=f"R$ {monthly_data['balance']:,.2f}",
            delta=f"R$ {monthly_data['balance']:,.2f}"
        )
    with col4:
        savings_rate = (monthly_data['balance'] / monthly_data['total_receitas'] * 100) if monthly_data['total_receitas'] > 0 else 0
        st.metric(
            label="Taxa de Poupança",
            value=f"{savings_rate:.1f}%"
        )
    
    st.divider()
    
    # Charts for the month
    col1, col2 = st.columns(2)
    
    with col1:
        if monthly_data['expenses_by_category']:
            st.subheader("📉 Despesas por Categoria")
            df_expenses = pd.DataFrame(monthly_data['expenses_by_category'])
            fig = px.pie(
                df_expenses, 
                values='total', 
                names='categoria',
                title="Distribuição das Despesas",
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma despesa encontrada para este mês.")
    
    with col2:
        if monthly_data['income_by_category']:
            st.subheader("📈 Receitas por Categoria")
            df_income = pd.DataFrame(monthly_data['income_by_category'])
            fig = px.pie(
                df_income, 
                values='total', 
                names='categoria',
                title="Distribuição das Receitas",
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma receita encontrada para este mês.")
    
    st.divider()
    
    # Yearly Summary
    st.subheader(f"📆 Resumo de {year}")
    
    yearly_data = get_yearly_summary(user_id, year)
    
    # Yearly KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Receitas Anual",
            value=f"R$ {yearly_data['total_receitas']:,.2f}"
        )
    with col2:
        st.metric(
            label="Total Despesas Anual",
            value=f"R$ {yearly_data['total_despesas']:,.2f}"
        )
    with col3:
        st.metric(
            label="Saldo Anual",
            value=f"R$ {yearly_data['balance']:,.2f}",
            delta=f"R$ {yearly_data['balance']:,.2f}"
        )
    
    # Yearly chart
    if yearly_data['monthly_data']:
        st.subheader("📊 Evolução Mensal")
        df_monthly = pd.DataFrame(yearly_data['monthly_data'])
        
        # Month names in Portuguese
        month_names = {
            1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
        }
        df_monthly['month_name'] = df_monthly['month'].map(month_names)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_monthly['month_name'],
            y=df_monthly['receitas'],
            name='Receitas',
            marker_color='#2E8B57'
        ))
        
        fig.add_trace(go.Bar(
            x=df_monthly['month_name'],
            y=df_monthly['despesas'],
            name='Despesas',
            marker_color='#DC143C'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_monthly['month_name'],
            y=df_monthly['balance'],
            name='Saldo',
            mode='lines+markers',
            line=dict(color='#1E90FF', width=3)
        ))
        
        fig.update_layout(
            title="Receitas, Despesas e Saldo Mensal",
            xaxis_title="Mês",
            yaxis_title="Valor (R$)",
            barmode='group',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para este ano.")
    
    st.divider()
    
    # Transaction list for the selected period
    st.subheader(f"📋 Transações de {datetime(2000, month, 1).strftime('%B')} de {year}")
    
    # Get transactions for the selected month/year
    conn = None
    try:
        import sqlite3
        import os
        DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'orbitfin.db')
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT id, tipo, valor, data, categoria, descricao, status
            FROM transactions
            WHERE user_id = ? 
            AND strftime('%Y', data) = ? 
            AND strftime('%m', data) = ?
            ORDER BY data DESC
            """,
            (user_id, str(year), f"{month:02d}")
        )
        
        rows = cursor.fetchall()
        transactions = [dict(row) for row in rows]
        
    except Exception as e:
        st.error(f"Erro ao carregar transações: {str(e)}")
        transactions = []
    finally:
        if conn:
            conn.close()
    
    if transactions:
        df = pd.DataFrame(transactions)
        df['valor'] = df['valor'].apply(lambda x: f"R$ {x:,.2f}")
        df['tipo'] = df['tipo'].map({'receita': '💰 Receita', 'despesa': '💸 Despesa'})
        df['status'] = df['status'].map({'pago': '✅ Pago', 'pendente': '⏳ Pendente'})
        
        # Rename columns for display
        df_display = df[['data', 'tipo', 'valor', 'categoria', 'descricao', 'status']].copy()
        df_display.columns = ['Data', 'Tipo', 'Valor', 'Categoria', 'Descrição', 'Status']
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma transação encontrada para este período.")

def show_configuracoes():
    import streamlit as st
    st.title("⚙️ Configurações")
    st.warning("Página de configurações ainda não implementada.")
    # Placeholder for future settings

if __name__ == "__main__":
    if not st.session_state.logged_in:
        apply_theme(hide_sidebar=True, auth=True)
        if st.session_state.auth_page == "register":
            render_register()
        else:
            render_login()
    else:
        main_app()