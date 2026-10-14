import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from services.sqlite_storage import (
    get_transactions,
    get_expenses_by_category,
    get_income_by_category,
    get_monthly_summary,
    get_yearly_summary
)

def main():
    # Initialize session state for user if not present (should be set by main app, but just in case)
    if 'user' not in st.session_state or not st.session_state.user:
        st.warning("Please log in to access the application.")
        return

    st.title("📊 Relatórios Financeiros")
    
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

if __name__ == "__main__":
    main()