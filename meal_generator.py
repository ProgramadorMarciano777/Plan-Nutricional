import openai
import streamlit as st
openai.api_key = st.secrets["OPENAI_KEY_API"]

def generate_meal_plan(user_data: dict, menu_input: str) -> str:
    TEMPLATE_PROMPT = f"""
Eres un nutricionista profesional y estás creando un plan de comidas adaptado al usuario. 
Toda la respuesta debe estar redactada en castellano (español de España).

Datos del cliente:
- Nombre: {user_data.get("nombre")}
- Edad: {user_data.get("edad")} años
- Sexo: {user_data.get("sexo")}
- Peso: {user_data.get("peso")} kg
- Estatura: {user_data.get("estatura")} cm
- IMC: {user_data.get("imc")}
- % Grasa corporal: {user_data.get("grasa")}
- % Masa muscular: {user_data.get("masa_muscular")}
- Objetivo nutricional principal: {user_data.get("objetivo")}

Preferencias del usuario: {user_data.get("preferences", "ninguna")}.
Restricciones del usuario: {user_data.get("restrictions", "ninguna")}.

Objetivos nutricionales diarios:
- Calorías diarias: {user_data["calories"]} kcal
- Proteína diaria: {user_data["protein"]}g
- Azúcar diaria: {user_data["sugar"]}g

Con los alimentos disponibles indicados a continuación, genera un plan de comidas que incluya:

👉 10 opciones diferentes para cada uno de los siguientes momentos del día:
- Desayuno
- Comida
- Cena
- Merienda o snack

Cada opción debe incluir:
- Nombre del plato (en negrita si es posible)
- Cantidad o ración exacta
- Valor calórico aproximado
- Breve receta o modo de preparación (si aplica)

Al final de cada bloque indica el total aproximado de calorías, proteínas, grasas, azúcares y carbohidratos.

Alimentos disponibles:
{menu_input}
"""
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un nutricionista profesional. Responde SIEMPRE en español de España."},
                {"role": "user", "content": TEMPLATE_PROMPT}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar el plan: {e}"
