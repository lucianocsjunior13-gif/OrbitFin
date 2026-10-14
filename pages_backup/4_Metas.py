import streamlit as st
from services.sqlite_storage import get_budgets, get_expenses_by_category

def show_goals():
    st.title("🎯 Metas de Economia")
    
    if 'user' not in st.session_state or not st.session_state.user:
        st.warning("Please log in to access the application.")
        return
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
            st.progress(min(gasto_atual / limite, 1.0))
            st.write(f"Gasto: R$ {gasto_atual:,.2f} de R$ {limite:,.2f}")
            st.write(f"Restante: R$ {restante:,.2f}")
            if restante <= 0:
                st.error("🎉 Meta atingida ou ultrapassada!")
            elif restante <= limite * 0.1:  # Less than 10% remaining
                st.warning("⚠️ Quase atingindo o limite")
            else:
                st.info(f"✅ Faltam R$ {restante:,.2f} para atingir a meta")
        else:
            st.write("Meta não definida (limite não informado)")
        
        st.divider()

if __name__ == "__main__":
    show_goals()