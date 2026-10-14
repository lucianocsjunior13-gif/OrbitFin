import streamlit as st
from services.sqlite_storage import (
    get_budgets, get_expenses_by_category, get_income_by_category, update_budget
)

def show_budget():
    st.title("📈 Orçamento e Categorias")
    
    if 'user' not in st.session_state or not st.session_state.user:
        st.warning("Please log in to access the application.")
        return
    user_id = st.session_state.user['id']
    
    # Get data
    budgets = get_budgets()
    expenses_by_category = get_expenses_by_category(user_id)
    income_by_category = get_income_by_category(user_id)
    
    st.subheader("📊 Limites por Categoria")
    
    for budget in budgets:
        categoria = budget.get('categoria', 'N/A')
        limite = float(budget.get('limite', 0))
        gasto_atual = float(expenses_by_category.get(categoria, 0))
        receita_atual = float(income_by_category.get(categoria, 0))
        percentual = (gasto_atual / limite * 100) if limite > 0 else 0
        
        st.write(f"**{categoria}**")
        
        # Progress bar
        progress = min(gasto_atual / limite, 1.0) if limite > 0 else 0
        st.progress(progress)
        
        # Details
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"Gasto: R$ {gasto_atual:,.2f}")
            if receita_atual > 0:
                st.write(f"Receita: R$ {receita_atual:,.2f}")
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

if __name__ == "__main__":
    show_budget()