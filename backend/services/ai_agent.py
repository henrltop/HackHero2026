import json
import os
from datetime import datetime, timezone

SYSTEM_PROMPT = """
Você é um agente de segurança parental. Analise a captura de tela
e identifique se o conteúdo é inadequado para crianças/adolescentes.

Gatilhos definidos pelos pais: {triggers}

Responda APENAS em JSON válido (sem markdown):
{{
  "nivel": "baixo|moderado|alto",
  "categoria": "categoria_especifica_em_snake_case",
  "descricao": "descrição curta em português explicando o que foi detectado",
  "confianca": 0.0
}}

Exemplos de categoria: seguro, violencia_ficcional_conflito, conteudo_adulto,
linguagem_ofensiva, apostas_jogos_dinheiro, drogas_alcool, bullying_assedio,
privacidade_dados_pessoais, malware_link_suspeito, outro_risco.

Use "seguro" quando não houver nenhum risco detectado.
"""

NIVEL_MAP = {
    "baixo":    "safe",
    "moderado": "attention",
    "alto":     "high_risk",
}

MOCK_REPORT_RAW = {
    "nivel":     "baixo",
    "categoria": "seguro",
    "descricao": "Conteúdo adequado — nenhum risco detectado (mock)",
    "confianca": 0.95,
}

RECOMMENDATIONS_PROMPT = """
Você é um especialista em segurança digital infantil e psicologia do desenvolvimento.
Com base nos alertas de monitoramento abaixo da criança/adolescente chamada {child_name},
gere de 3 a 5 recomendações práticas e empáticas para os pais.

Alertas recentes:
{alerts_summary}

Responda APENAS em JSON válido (sem markdown):
{{
  "recommendations": [
    "recomendação 1",
    "recomendação 2",
    "recomendação 3"
  ]
}}
"""

MOCK_RECOMMENDATIONS = [
    "Converse abertamente com seu filho sobre os conteúdos que ele acessa online.",
    "Estabeleça horários combinados para uso do celular, especialmente antes de dormir.",
    "Considere atividades offline juntos para fortalecer o vínculo familiar.",
]


def _build_response(raw: dict, app_package: str) -> dict:
    """Converte o output bruto da IA no formato padrão da API."""
    nivel = raw.get("nivel", "baixo")
    return {
        "app":               app_package or "desconhecido",
        "categoria":         raw.get("categoria", "seguro"),
        "nivel":             nivel,
        "risk_level":        NIVEL_MAP.get(nivel, "safe"),
        "descricao":         raw.get("descricao", ""),
        "confianca":         raw.get("confianca", 0.0),
        "timestamp":         datetime.now(timezone.utc).isoformat(),
        "imagem_armazenada": False,
        "analise":           "gemini-2.5-flash",
    }


def analyze_image(image_bytes: bytes, triggers: list[str], app_package: str = "") -> dict:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return _build_response(MOCK_REPORT_RAW, app_package)

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

        raw = json.loads(text)
        return _build_response(raw, app_package)

    except Exception:
        return _build_response(MOCK_REPORT_RAW, app_package)
    finally:
        del image_bytes


def generate_recommendations(child_name: str, alerts: list[dict]) -> list[str]:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return MOCK_RECOMMENDATIONS

    try:
        from google import genai

        alerts_summary = "\n".join(
            f"- [{a.get('nivel', a.get('risk_level', '?'))}] {a['description']} "
            f"(app: {a.get('app_package', 'desconhecido')})"
            for a in alerts
        )
        prompt = RECOMMENDATIONS_PROMPT.format(child_name=child_name, alerts_summary=alerts_summary)

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        return json.loads(text).get("recommendations", MOCK_RECOMMENDATIONS)
    except Exception:
        return MOCK_RECOMMENDATIONS
