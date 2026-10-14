import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from services.sqlite_storage import (
    get_transactions, get_budgets, get_insights, get_expenses_by_category
)

def show_dashboard():
    # Get user id from session state
    if 'user' not in st.session_state or not st.session_state.user:
        st.warning("Usuário não autenticado")
        return
    user_id = st.session_state.user['id']
    
    # Get data
    transactions = get_transactions(user_id)
    budgets = get_budgets()
    insights = get_insights()
    expenses_by_cat = get_expenses_by_category(user_id)
    
    # Calculate KPIs
    total_balance = sum(
        t['valor'] if t['tipo'] == 'receita' else -t['valor']
        for t in transactions
    )
    
    monthly_expenses = sum(
        t['valor'] for t in transactions 
        if t['tipo'] == 'despesa' and 
        datetime.fromisoformat(t['data']).month == datetime.now().month and
        datetime.fromisoformat(t['data']).year == datetime.now().year
    )
    
    monthly_income = sum(
        t['valor'] for t in transactions 
        if t['tipo'] == 'receita' and 
        datetime.fromisoformat(t['data']).month == datetime.now().month and
        datetime.fromisoformat(t['data']).year == datetime.now().year
    )
    
    # Custom CSS to match the HTML design
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background: var(--background-color);
    }
    .sidebar .sidebar-content .block-container {
        padding-top: 2rem;
    }
    .sidebar .sidebar-content .stButton>button {
        width: 100%;
        border-radius: 8px;
        margin: 5px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px;
        font-weight: 600;
        transition: transform 0.2s;
    }
    .sidebar .sidebar-content .stButton>button:hover {
        transform: translateY(-2px);
    }
    .sidebar .sidebar-content .stButton>button:active {
        transform: translateY(0);
    }
    .sidebar .sidebar-content .stSelectbox>div>div>div>div {
        background-color: white;
        border-radius: 8px;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .dashboard-container {
        max-width: 1200px;
        margin: 0 auto;
    }
    .welcome {
        text-align: center;
        margin-bottom: 2rem;
    }
    .welcome h1 {
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }
    .welcome p {
        color: var(--text-color-light);
        font-size: 1.1rem;
    }
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    .card {
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        overflow: hidden;
        border: 1px solid #f1f5f9;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        border-color: #e2e8f0;
    }
    .card h3 {
        margin: 0 0 1rem 0;
        padding: 1.5rem 1.5rem 0 1.5rem;
        color: var(--secondary-color);
        font-size: 1.25rem;
        font-weight: 600;
    }
    .card .valor {
        font-size: 2rem;
        font-weight: 700;
        color: var(--secondary-color);
        margin: 0 1.5rem;
        text-align: center;
    }
    .card .chart-card, .card .limits-card {
        padding: 1.5rem;
    }
    .card .card-content {
        padding: 1.5rem;
    }
    .card .card-bottom-bar {
        height: 4px;
        background: linear-gradient(90deg, #ff9a56, #ff6a7a);
        margin-top: auto;
    }
    .sidebar-divider {
        border-top: 1px solid #eee;
        margin: 1.5rem 0;
    }
    .sidebar-top, .sidebar-bottom {
        padding: 1.5rem;
    }
    .sidebar-logo h2 {
        color: var(--secondary-color);
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }
    .sidebar-user-profile {
        display: flex;
        align-items: center;
        margin-top: 1rem;
    }
    .sidebar-avatar {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        margin-right: 1rem;
    }
    .sidebar-user-info {
        flex: 1;
    }
    .sidebar-name {
        font-weight: 600;
        color: var(--text-color);
    }
    .sidebar-role {
        color: var(--text-color-light);
        font-size: 0.9rem;
    }
    .main-nav button {
        width: 100%;
        text-align: left;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        background: #f8fafc;
        border: 1px solid #eee;
        color: var(--text-color);
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .main-nav button:hover {
        background: #f1f5f9;
        border-color: #e2e8f0;
    }
    .main-nav button[kind="secondary"] {
        background: white;
        border-color: #ddd;
    }
    .main-nav button[kind="secondary"]:hover {
        background: #f8fafc;
    }
    .footer-nav button {
        width: 100%;
        text-align: left;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        background: #f8fafc;
        border: 1px solid #eee;
        color: var(--text-color);
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .footer-nav button:hover {
        background: #f1f5f9;
        border-color: #e2e8f0;
    }
    .stMetric {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
    .stMetric label {
        color: var(--text-color-light);
        font-weight: 500;
        font-size: 0.9rem;
    }
    .stMetric div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--secondary-color);
    }
    .stMetric div[data-testid="stMetricDelta"] {
        font-size: 0.9rem;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-top">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
        st.markdown('<h2>OrbitFin</h2>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # User profile
        user_name = st.session_state.user['name']
        first_initial = user_name[0].upper() if user_name else '?'
        last_initial = user_name.split()[-1][0].upper() if len(user_name.split()) > 1 else '?'
        avatar_text = f"{first_initial}{last_initial}"
        st.markdown(f'''
        <div class="sidebar-user-profile">
            <div class="sidebar-avatar">{avatar_text}</div>
            <div class="sidebar-user-info">
                <div class="sidebar-name">{user_name}</div>
                <div class="sidebar-role">Usuário</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Main navigation
        st.markdown('<nav class="main-nav">', unsafe_allow_html=True)
        nav_items = [
            ("📊", "Dashboard", "dashboard"),
            ("💰", "Transações", "transacoes"),
            ("📈", "Orçamento", "orcamento"),
            ("🎯", "Metas", "metas"),
            ("📊", "Relatórios", "relatorios"),
            ("⚙️", "Configurações", "configuracoes")
        ]
        
        for icon, label, page in nav_items:
            if st.button(f"{icon} {label}", key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()
        
        st.markdown('</nav>', unsafe_allow_html=True)
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Footer nav for settings (isolated as in HTML)
        st.markdown('<nav class="footer-nav">', unsafe_allow_html=True)
        if st.button("⚙️ Configurações", key="nav_configuracoes_footer"):
            st.session_state.page = "configuracoes"
            st.rerun()
        st.markdown('</nav>', unsafe_allow_html=True)
    
    # Main content
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Header
    user_first_name = st.session_state.user['name'].split()[0] if st.session_state.user['name'] else 'Usuário'
    st.markdown(f'''
    <header class="welcome">
        <h1>Bem-vindo, <span id="welcomeName">{user_first_name}!</span></h1>
        <p>Seu resumo financeiro em tempo real</p>
    </header>
    ''', unsafe_allow_html=True)
    
    # Upper Grid (3 columns) - Dashboard cards
    st.markdown('<div class="dashboard-grid upper-grid">', unsafe_allow_html=True)
    
    # Card 1: Saldo Total
    st.markdown(f'''
    <section class="card saldo-total-card">
        <h3>Saldo Total</h3>
        <p class="valor" id="totalBalance">R$ {total_balance:,.2f}</p>
        <div class="bancos-conectados">
            <div class="banco-badge">
                <i class="fi fi-br-wallet"></i>
            </div>
            <span class="texto-contas" id="connectedAccounts">0 contas conectadas</span>
        </div>
        <div class="card-bottom-bar"></div>
    </section>
    ''', unsafe_allow_html=True)
    
    # Card 2: Receitas e Despesas
    st.markdown('''
    <section class="card chart-card">
        <h3>Receitas vs Despesas</h3>
        <div class="chart-container">
            <div class="bars-wrapper" id="barsWrapper">
                <!-- Bars will be injected here -->
            </div>
        </div>
        <div class="chart-legend" id="chartLegend">
            <!-- Legend will be injected here -->
        </div>
        <div class="card-bottom-bar"></div>
    </section>
    ''', unsafe_allow_html=True)
    
    # Card 3: Limites de Gastos
    st.markdown('''
    <section class="card limits-card">
        <h3>Limites de Gastos</h3>
        <div class="filter-container">
            <label for="categorySelect">Categoria:</label>
            <select id="categorySelect" onchange="updateLimitChart()">
                <!-- Options will be injected here -->
            </select>
        </div>
        <div class="line-chart-container">
            <svg class="line-svg" viewBox="0 0 300 100" preserveAspectRatio="none">
                <path id="limitChartPath" d="M 10,75 Q 80,20 150,45 T 290,65" fill="none" stroke="#E05638" stroke-width="3" stroke-linecap="round" />
            </svg>
        </div>
        <div class="chart-months" id="limitChartMonths">
            <span>Jul</span><span>Ago</span><span>Set</span><span>Out</span><span>Nov</span><span>Dez</span>
        </div>
        <div class="card-bottom-bar"></div>
    </section>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close upper-grid
    
    # Lower Grid (3 columns / blocos)
    st.markdown('<div class="dashboard-grid lower-grid">', unsafe_allow_html=True)
    
    # Card 4: Transações Recentes
    st.markdown('''
    <section class="card">
        <h2>Transações Recentes</h2>
        <div class="card-content">
            <table class="transactions-table">
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>Descrição</th>
                        <th>Valor</th>
                    </tr>
                </thead>
                <tbody id="recentTransactionsBody">
                    <!-- Rows will be injected here -->
                </tbody>
            </table>
        </div>
    </section>
    ''', unsafe_allow_html=True)
    
    # Card 5: Gastos por Categoria
    st.markdown('''
    <section class="card">
        <h2>Gastos por Categoria</h2>
        <div class="card-content" id="categoryExpensesContainer">
            <!-- Progress categories will be injected here -->
        </div>
    </section>
    ''', unsafe_allow_html=True)
    
    # Card 6: AI Insights - Removed as per request to remove static/fictitious values
    # If you want to keep a dynamic insights section, you can add it later based on actual data analysis
    st.markdown('''
    <section class="card">
        <h2>Insights</h2>
        <div class="card-content" id="insightsContainer">
            <!-- Insights will be injected here -->
        </div>
    </section>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close lower-grid
    st.markdown('</div>', unsafe_allow_html=True)  # Close dashboard-container
    
    # Now we need to inject the actual Streamlit components where placeholders are
    # We'll use Streamlit's native components but position them to replace the placeholders
    # We'll use a combination of st.markdown with HTML and st.components.v1.html if needed, but for simplicity,
    # we'll display the actual content using Streamlit components below the HTML placeholders.
    
    st.divider()
    
    # KPIs display using Streamlit but styled
    col1, col2, col3 = st.columns(3)
    
    with col1:
        delta_color = "normal" if total_balance >= 0 else "inverse"
        st.metric(
            label="Saldo Total",
            value=f"R$ {total_balance:,.2f}",
            delta=f"R$ {total_balance:,.2f}" if total_balance >= 0 else f"-R$ {abs(total_balance):,.2f}",
            delta_color=delta_color
        )
    
    with col2:
        st.metric(
            label="Despesas do Mês",
            value=f"R$ {monthly_expenses:,.2f}",
            delta=f"-R$ {monthly_expenses:,.2f}"
        )
    
    with col3:
        st.metric(
            label="Receitas do Mês",
            value=f"R$ {monthly_income:,.2f}",
            delta=f"R$ {monthly_income:,.2f}"
        )
    
    st.divider()
    
    # Charts
    if transactions:
        # Receitas vs Despesas chart
        st.subheader("Receitas vs Despesas Mensais")
        df = pd.DataFrame(transactions)
        df['data'] = pd.to_datetime(df['data'])
        df['mês'] = df['data'].dt.to_period('M')
        
        chart_data = df.groupby(['mês', 'tipo'])['valor'].sum().reset_index()
        chart_data['mês_str'] = chart_data['mês'].astype(str)
        
        fig = px.bar(
            chart_data, 
            x='mês_str', 
            y='valor', 
            color='tipo',
            title="Receitas vs Despesas por Mês",
            labels={'mês_str': 'Mês', 'valor': 'Valor (R$)', 'tipo': 'Tipo'},
            color_discrete_map={'receita': '#2E8B57', 'despesa': '#DC143C'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Limits chart (simplified)
        st.subheader("Limites de Gastos")
        expenses_by_cat = get_expenses_by_category(user_id)
        if expenses_by_cat:
            # Create a simple bar chart for expenses by category
            df_expenses = pd.DataFrame(list(expenses_by_cat.items()), columns=['Categoria', 'Valor'])
            df_expenses = df_expenses.sort_values('Valor', ascending=False)
            
            fig = px.bar(
                df_expenses,
                x='Categoria',
                y='Valor',
                title="Gastos por Categoria",
                color='Valor',
                color_continuous_scale='Reds'
            )
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma despesa encontrada.")
    else:
        st.info("Nenhuma transação encontrada. Comece adicionando algumas transações!")
    
    st.divider()
    
    # Insights
    st.subheader("💡 Insight do Dia")
    if insights and 'texto' in insights:
        st.info(insights['texto'])
    else:
        st.info("Mantenha um registro regular de suas transações para melhor controle financeiro.")

# The main app logic is handled in app.py, so this function is called from there.
# We'll keep the function as is for now.