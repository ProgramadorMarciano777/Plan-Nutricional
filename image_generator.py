import openai

# Usa la misma API KEY ya configurada en el entorno
openai.api_key = os.getenv("OPENAI_KEY_API")

def generate_image_from_prompt(prompt: str) -> str:
  try:
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.images.generate(
      model = "dall-e-3",
      prompt = prompt,
      size = "512x512",
      quality = "standard",
      n = 1
    )
    return response.data[0].url
  except Exception as e:
    return None
