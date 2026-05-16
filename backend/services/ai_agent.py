import base64
import json
import os

SYSTEM_PROMPT = """
Você é um agente de segurança parental. Analise a captura de tela
e identifique se o conteúdo é inadequado para crianças/adolescentes.

Gatilhos definidos pelos pais: {triggers}

Responda APENAS em JSON válido (sem markdown):
{{
  "risk_level": "safe|attention|high_risk",
  "confidence": 0.0,
  "detected_triggers": [],
  "description": "descrição curta em português"
}}
"""

MOCK_REPORT = {
    "risk_level": "safe",
    "confidence": 0.95,
    "detected_triggers": [],
    "description": "Conteúdo adequado — nenhum risco detectado (mock)",
}


def analyze_image(image_bytes: bytes, triggers: list[str]) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return MOCK_REPORT

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        prompt = SYSTEM_PROMPT.format(triggers=", ".join(triggers) if triggers else "nenhum")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            ],
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        return json.loads(text)
    except Exception:
        return MOCK_REPORT
    finally:
        del image_bytes
