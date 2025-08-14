import streamlit as st
from meal_generator import generate_meal_plan
import re
from docx import Document

# -------- Helpers --------
def _to_float(x):
    if x is None: 
        return None
    x = str(x).strip().replace(',', '.')
    try:
        return float(x)
    except:
        return None

def parse_docx(file) -> dict:
    """
    Espera líneas tipo:
    Nombre completo: ...
    Edad: 30
    Sexo: Hombre/Mujer
    Peso (kg): 78
    Estatura (cm): 175
    IMC: 25.5
    % Grasa corporal: 18
    % Masa muscular: 40
    Objetivo nutricional principal: Pérdida de grasa
    """
    doc = Document(file)
    text = "\n".join(p.text for p in doc.paragraphs)

    def get(label):
        # Busca "Label:" con may/min, acentos y espacios flexibles
        import re
        pattern = rf"{label}\s*:\s*(.+)"
        m = re.search(pattern, text, flags=re.IGNORECASE)
        return m.group(1).strip() if m else None

    data = {
        "nombre": get(r"Nombre completo"),
        "edad": _to_float(get(r"Edad")),
        "sexo": get(r"Sexo"),
        "peso": _to_float(get(r"Peso\s*\(kg\)")),
        "estatura": _to_float(get(r"Estatura\s*\(cm\)")),
        "imc": _to_float(get(r"IMC")),
        "grasa": _to_float(get(r"%\s*Grasa\s*corporal")),
        "masa_muscular": _to_float(get(r"%\s*Masa\s*muscular")),
        "objetivo": get(r"Objetivo\s*nutricional\s*principal"),
    }

    # Si falta IMC y tenemos peso/estatura, lo calculamos (altura en metros)
    if data.get("imc") is None and data.get("peso") and data.get("estatura"):
        h_m = data["estatura"] / 100.0
        if h_m > 0:
            data["imc"] = round(data["peso"] / (h_m**2), 1)

    return data

# -------- UI --------
st.title("🥗 NutriGen - Generador Nutricional Interactivo")

# 1) Subir ficha de Word
uploaded = st.file_uploader("Sube la ficha del cliente (.docx)", type=["docx"])

# 2) Parsear y mostrar un resumen rápido
parsed = {}
if uploaded is not None:
    try:
        parsed = parse_docx(uploaded) or {}
        with st.expander("📄 Datos importados del documento"):
            st.write(parsed)
    except Exception as e:
        st.error(f"No se pudo leer el documento: {e}")

# 3) Form con valores por defecto desde el .docx (si existen)
with st.form("nutri_form"):
    st.subheader("Introduce / revisa los datos")

    nombre = st.text_input("Nombre completo", value=parsed.get("nombre", "") or "")
    edad = st.number_input("Edad", 0, 120, int(parsed.get("edad") or 30))
    sexo = st.selectbox("Sexo", ["Hombre", "Mujer", "Otro"], 
                        index={"hombre":0,"mujer":1}.get(str(parsed.get("sexo") or "").lower(), 2))

    weight_default = float(parsed.get("peso") or 70.0)
    height_default = float(parsed.get("estatura") or 170.0)

    weight = st.number_input("Peso (kg)", 30.0, 300.0, weight_default)
    height = st.number_input("Estatura (cm)", 120.0, 230.0, height_default)

    imc_val = parsed.get("imc")
    st.markdown(f"**IMC (auto):** {imc_val if imc_val is not None else '—'}")

    grasa = st.number_input("% Grasa corporal", 0.0, 70.0, float(parsed.get("grasa") or 0.0))
    masa = st.number_input("% Masa muscular", 0.0, 80.0, float(parsed.get("masa_muscular") or 0.0))

    objetivo = st.text_input("Objetivo nutricional principal", value=parsed.get("objetivo", "") or "")

    st.markdown("---")
    st.subheader("Parámetros del plan")
    preferences = st.text_input("Preferencias alimentarias (ej. mediterránea, vegana...)")
    restrictions = st.text_input("Restricciones (ej. sin gluten, sin lactosa...)")
    calories = st.number_input("Calorías diarias objetivo", 1000, 5000, 2000)
    protein = st.number_input("Proteína diaria objetivo (g)", 20, 300, 120)
    sugar = st.number_input("Azúcar diaria objetivo (g)", 0, 200, 30)
    menu_input = st.text_area("Lista de alimentos disponibles (ej. Arroz = 100, Pollo = 200...)")

    submitted = st.form_submit_button("Generar Plan")

# 4) Generar plan
if submitted:
    user_data = {
        "nombre": nombre,
        "edad": edad,
        "sexo": sexo,
        "peso": weight,
        "estatura": height,
        "imc": imc_val,
        "grasa": grasa,
        "masa_muscular": masa,
        "objetivo": objetivo,
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
