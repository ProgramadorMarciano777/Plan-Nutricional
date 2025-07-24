import streamlit as st
from meal_generator import generate_meal_plan
from image_generator import generate_image_from_prompt
import re

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
        st.session_state["raw_plan"] = plan

        st.markdown("---")
        blocks = re.split(r"\n-{3,}\n", plan) if "---" in plan else [plan]

        for block in blocks:
            st.markdown(block)
            # Buscar descripciones visuales dentro del bloque
            matches = re.findall(r"(?i)descripción visual: (.+)", block)
            for desc in matches:
                image_url = generate_image_from_prompt(desc.strip())
                if image_url:
                    st.image(image_url, caption=desc.strip(), use_column_width="always")
                else:
                    st.warning("❌ Error al generar la imagen.")