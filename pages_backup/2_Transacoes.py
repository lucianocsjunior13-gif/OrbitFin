import streamlit as st
import pandas as pd
from datetime import datetime
from services.sqlite_storage import (
    get_transactions, add_transaction, update_transaction, delete_transaction
)

def show_transactions():
    # Get user id from session state
    if 'user' not in st.session_state or not st.session_state.user:
        st.warning("Usuário não autenticado")
        return
    user_id = st.session_state.user['id']
    
    # Get transactions
    transactions = get_transactions(user_id)
    
    # Initialize session state for editing and adding
    if 'editing_idx' not in st.session_state:
        st.session_state.editing_idx = None
    if 'adding_receita' not in st.session_state:
        st.session_state.adding_receita = False
    if 'adding_despesa' not in st.session_state:
        st.session_state.adding_despesa = False
    
    # Custom CSS for compact layout
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        margin: 2px 0;
    }
    .stSelectbox>div>div>div>div {
        border-radius: 6px;
    }
    .stTextInput>div>div>input {
        border-radius: 6px;
    }
    .stDateInput>div>div>input {
        border-radius: 6px;
    }
    .stNumberInput>div>div>input {
        border-radius: 6px;
    }
    .stExpander {
        border: 1px solid #eee;
        border-radius: 8px;
        margin: 10px 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 6px 6px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: white;
        border-bottom: 2px solid #ff6b6b;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.header("Gerenciamento de Transações")
    st.caption("Visualize, filtre e adicione suas movimentações financeiras")
    
    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("Buscar:", placeholder="Descrição, estabelecimento...")
    with col2:
        # Get unique categories for filter
        if transactions:
            categorias = ["Todas"] + sorted(list(set(t.get('categoria', '') for t in transactions if t.get('categoria'))))
        else:
            categorias = ["Todas"]
        categoria_filter = st.selectbox("Categoria:", categorias)
    with col3:
        date_filter = st.date_input("Data:", value=None)
    
    # Buttons for adding transactions
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("💰 Nova Receita", use_container_width=True):
            st.session_state.adding_receita = True
            st.session_state.adding_despesa = False
    with col2:
        if st.button("💸 Nova Despesa", use_container_width=True):
            st.session_state.adding_despesa = True
            st.session_state.adding_receita = False
    with col3:
        st.write("")  # spacer
    
    # Form for adding transaction (receita or despesa)
    if st.session_state.adding_receita or st.session_state.adding_despesa:
        tipo = "receita" if st.session_state.adding_receita else "despesa"
        title = "Nova Receita" if st.session_state.adding_receita else "Nova Despesa"
        with st.expander(title, expanded=True):
            with st.form(key=f"form_{tipo}"):
                descricao = st.text_input("Descrição*", placeholder="Ex: Salário, Supermercado")
                col1, col2 = st.columns(2)
                with col1:
                    valor = st.number_input("Valor (R$)*", min_value=0.01, step=0.01, format="%.2f")
                with col2:
                    data = st.date_input("Data*", value=datetime.now())
                # Category options based on type
                if tipo == "receita":
                    categoria_options = ["Selecione uma categoria", "Salário", "Freelance", "Investimentos", "Outros"]
                    categoria_keys = ["", "salario", "freelance", "investimentos", "outros"]
                else:
                    categoria_options = ["Selecione uma categoria", "Alimentação", "Transporte", "Lazer", "Moradia", "Saúde", "Educação", "Outros"]
                    categoria_keys = ["", "alimentacao", "transporte", "lazer", "moradia", "saude", "educacao", "outros"]
                categoria = st.selectbox("Categoria*", options=categoria_options)
                # We don't have account management in our simplified model, so skip
                submitted = st.form_submit_button("Salvar")
                if submitted:
                    if not descricao or not valor or categoria == "Selecione uma categoria":
                        st.error("Por favor, preencha todos os campos obrigatórios.")
                    else:
                        categoria_key = categoria_keys[categoria_options.index(categoria)]
                        transaction_data = {
                            "tipo": tipo,
                            "valor": float(valor),
                            "data": data.strftime("%Y-%m-%d"),
                            "categoria": categoria_key,
                            "descricao": descricao,
                            "status": "pago"
                        }
                        try:
                            added = add_transaction(user_id, transaction_data)
                            if added:
                                st.success(f"{title} adicionada com sucesso!")
                                st.session_state.adding_receita = False
                                st.session_state.adding_despesa = False
                                st.rerun()
                            else:
                                st.error("Erro ao adicionar transação.")
                        except Exception as e:
                            st.error(f"Erro: {e}")
    
    # Apply filters
    filtered = transactions.copy()
    if search_term:
        filtered = [t for t in filtered if search_term.lower() in t.get('descricao', '').lower()]
    if categoria_filter != "Todas":
        filtered = [t for t in filtered if t.get('categoria') == categoria_filter]
    if date_filter:
        filtered = [t for t in filtered if t.get('data') == date_filter.strftime("%Y-%m-%d")]
    
    # Split by type for tabs
    receitas = [t for t in filtered if t.get('tipo') == 'receita']
    despesas = [t for t in filtered if t.get('tipo') == 'despesa']
    
    # Tabs
    tab1, tab2 = st.tabs(["📥 Receitas", "📤 Despesas"])
    
    with tab1:
        st.subheader(f"Receitas ({len(receitas)} items)")
        if receitas:
            # Display table with edit/delete
            for idx, t in enumerate(receitas):
                with st.container():
                    col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 2, 2, 2, 2])
                    with col1:
                        st.write(t.get('data', ''))
                    with col2:
                        st.write(t.get('descricao', ''))
                    with col3:
                        st.write(t.get('categoria', ''))
                    with col4:
                        st.write("")  # Conta placeholder
                    with col5:
                        valor = t.get('valor', 0)
                        st.markdown(f"<span style='color: #2E8B57; font-weight: 600;'>+ R$ {valor:,.2f}</span>", unsafe_allow_html=True)
                    with col6:
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            if st.button("✏️ Editar", key=f"edit_receita_{idx}"):
                                st.session_state.editing_idx = ('receita', idx)
                                st.rerun()
                        with btn_col2:
                            if st.button("🗑️ Excluir", key=f"delete_receita_{idx}"):
                                t_id = t.get('id')
                                if t_id and delete_transaction(user_id, t_id):
                                    st.success("Transação excluída!")
                                    st.rerun()
                                else:
                                    st.error("Erro ao excluir transação.")
                    # Editing form
                    if st.session_state.editing_idx and st.session_state.editing_idx[0] == 'receita' and st.session_state.editing_idx[1] == idx:
                        t = receitas[idx]
                        with st.form(key=f"edit_form_receita_{idx}"):
                            edit_descricao = st.text_input("Descrição", value=t.get('descricao', ''))
                            col1, col2 = st.columns(2)
                            with col1:
                                edit_valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, value=float(t.get('valor', 0)), format="%.2f")
                            with col2:
                                edit_data = st.date_input("Data", value=datetime.strptime(t.get('data', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d'))
                            categoria_options = ["Selecione uma categoria", "Salário", "Freelance", "Investimentos", "Outros"]
                            categoria_keys = ["", "salario", "freelance", "investimentos", "outros"]
                            current_categoria = t.get('categoria', '')
                            # Find index
                            try:
                                cat_idx = categoria_keys.index(current_categoria) if current_categoria in categoria_keys else 0
                            except ValueError:
                                cat_idx = 0
                            edit_categoria = st.selectbox("Categoria", options=categoria_options, index=cat_idx)
                            submitted = st.form_submit_button("Salvar Alterações")
                            if submitted:
                                if not edit_descricao or not edit_valor or edit_categoria == "Selecione uma categoria":
                                    st.error("Por favor, preencha todos os campos obrigatórios.")
                                else:
                                    categoria_key = categoria_keys[categoria_options.index(edit_categoria)]
                                    update_data = {
                                        "tipo": "receita",
                                        "valor": float(edit_valor),
                                        "data": edit_data.strftime("%Y-%m-%d"),
                                        "categoria": categoria_key,
                                        "descricao": edit_descricao,
                                        "status": "pago"
                                    }
                                    try:
                                        updated = update_transaction(user_id, t.get('id'), update_data)
                                        if updated:
                                            st.success("Transação atualizada!")
                                            st.session_state.editing_idx = None
                                            st.rerun()
                                        else:
                                            st.error("Erro ao atualizar transação.")
                                    except Exception as e:
                                        st.error(f"Erro: {e}")
                            cancel_btn = st.form_submit_button("Cancelar")
                            if cancel_btn:
                                st.session_state.editing_idx = None
                                st.rerun()
        else:
            st.info("Nenhuma receita encontrada.")
    
    with tab2:
        st.subheader(f"Despesas ({len(despesas)} items)")
        if despesas:
            for idx, t in enumerate(despesas):
                with st.container():
                    col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 2, 2, 2, 2])
                    with col1:
                        st.write(t.get('data', ''))
                    with col2:
                        st.write(t.get('descricao', ''))
                    with col3:
                        st.write(t.get('categoria', ''))
                    with col4:
                        st.write("")  # Conta placeholder
                    with col5:
                        valor = t.get('valor', 0)
                        st.markdown(f"<span style='color: #DC143C; font-weight: 600;'>- R$ {valor:,.2f}</span>", unsafe_allow_html=True)
                    with col6:
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            if st.button("✏️ Editar", key=f"edit_despesa_{idx}"):
                                st.session_state.editing_idx = ('despesa', idx)
                                st.rerun()
                        with btn_col2:
                            if st.button("🗑️ Excluir", key=f"delete_despesa_{idx}"):
                                t_id = t.get('id')
                                if t_id and delete_transaction(user_id, t_id):
                                    st.success("Transação excluída!")
                                    st.rerun()
                                else:
                                    st.error("Erro ao excluir transação.")
                    # Editing form
                    if st.session_state.editing_idx and st.session_state.editing_idx[0] == 'despesa' and st.session_state.editing_idx[1] == idx:
                        t = despesas[idx]
                        with st.form(key=f"edit_form_despesa_{idx}"):
                            edit_descricao = st.text_input("Descrição", value=t.get('descricao', ''))
                            col1, col2 = st.columns(2)
                            with col1:
                                edit_valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, value=float(t.get('valor', 0)), format="%.2f")
                            with col2:
                                edit_data = st.date_input("Data", value=datetime.strptime(t.get('data', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d'))
                            categoria_options = ["Selecione uma categoria", "Alimentação", "Transporte", "Lazer", "Moradia", "Saúde", "Educação", "Outros"]
                            categoria_keys = ["", "alimentacao", "transporte", "lazer", "moradia", "saude", "educacao", "outros"]
                            current_categoria = t.get('categoria', '')
                            try:
                                cat_idx = categoria_keys.index(current_categoria) if current_categoria in categoria_keys else 0
                            except ValueError:
                                cat_idx = 0
                            edit_categoria = st.selectbox("Categoria", options=categoria_options, index=cat_idx)
                            submitted = st.form_submit_button("Salvar Alterações")
                            if submitted:
                                if not edit_descricao or not edit_valor or edit_categoria == "Selecione uma categoria":
                                    st.error("Por favor, preencha todos os campos obrigatórios.")
                                else:
                                    categoria_key = categoria_keys[categoria_options.index(edit_categoria)]
                                    update_data = {
                                        "tipo": "despesa",
                                        "valor": float(edit_valor),
                                        "data": edit_data.strftime("%Y-%m-%d"),
                                        "categoria": categoria_key,
                                        "descricao": edit_descricao,
                                        "status": "pago"
                                    }
                                    try:
                                        updated = update_transaction(user_id, t.get('id'), update_data)
                                        if updated:
                                            st.success("Transação atualizada!")
                                            st.session_state.editing_idx = None
                                            st.rerun()
                                        else:
                                            st.error("Erro ao atualizar transação.")
                                    except Exception as e:
                                        st.error(f"Erro: {e}")
                            cancel_btn = st.form_submit_button("Cancelar")
                            if cancel_btn:
                                st.session_state.editing_idx = None
                                st.rerun()
        else:
            st.info("Nenhuma despesa encontrada.")

if __name__ == "__main__":
    show_transactions()