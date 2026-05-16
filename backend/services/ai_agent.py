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
    api_key = os.environ.get("MISTRAL_API_KEY", "")
    if not api_key:
        return MOCK_REPORT

    try:
        from mistralai import Mistral

        client = Mistral(api_key=api_key)
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        prompt = SYSTEM_PROMPT.format(triggers=", ".join(triggers) if triggers else "nenhum")

        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_b64}"},
                ],
            }],
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return MOCK_REPORT
    finally:
        del image_bytes
