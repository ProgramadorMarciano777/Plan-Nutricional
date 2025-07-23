import openai

# Mete aquí tu clave directamente
openai.api_key = "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"

def generate_meal_plan(user_data: dict, menu_input: str) -> str:
    TEMPLATE_PROMPT = f"""
Eres un nutricionista profesional y estás creando un plan de comidas adaptado al usuario. Toda la respuesta debe estar redactada en castellano (español de España).

Preferencias del usuario: {user_data.get("preferences", "ninguna")}.
Restricciones del usuario: {user_data.get("restrictions", "ninguna")}.
Objetivos del usuario:
- Calorías diarias: {user_data["calories"]} kcal
- Proteína diaria: {user_data["protein"]}g
- Azúcar diaria: {user_data["sugar"]}g

Con los alimentos disponibles indicados a continuación, genera un plan de comidas que incluya:

👉 **3 opciones diferentes para cada uno de los siguientes momentos del día**:
- Desayuno
- Comida
- Cena
- Merienda o snack

Cada opción debe incluir:
- Nombre del plato
- Cantidad o ración exacta (por ejemplo: “1 filete de pollo de 150g”)
- Valor calórico aproximado
- Breve receta o modo de preparación (si aplica)

Después de cada bloque (desayunos, comidas, etc.), indica el total aproximado de calorías, proteínas y azúcares del conjunto.

Available items:
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
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar el plan: {e}"
