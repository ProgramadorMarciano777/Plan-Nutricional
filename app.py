import streamlit as st
from meal_generator import generate_meal_plan

st.title("🥗 NutriGen - Generador Nutricional Interactivo")

with st.form("nutri_form"):
    st.subheader("Introduce tus datos")

    preferences = st.text_input("Preferencias alimentarias (ej. comida mediterránea, vegana...)")
    restrictions = st.text_input("Restricciones (ej. sin gluten, sin lactosa...)")
    calories = st.number_input("Calorías diarias objetivo", 1000, 5000, 2000)
    protein = st.number_input("Proteína diaria objetivo (g)", 20, 300, 120)
    sugar = st.number_input("Azúcar diario objetivo (g)", 0, 100, 30)
    menu_input = st.text_area("Lista de alimentos disponibles (ej. Arroz = 100, Pollo = 200...)")

    submitted = st.form_submit_button("Generar Plan")

if submitted:
    user_data = {
        "preferences": preferences,
        "restrictions": restrictions,
        "calories": calories,
        "protein": protein,
        "sugar": sugar
    }
    st.markdown("### 🧠 Resultado:")
    with st.spinner("Generando el plan..."):
        plan = generate_meal_plan(user_data, menu_input)
        st.text_area("Plan generado:", plan, height=500)
