import json
import os
from datetime import datetime, timezone

# Categorias baseadas em PEGI 2026, ESRB, WHO ICD-11, ECA Digital e SaferNet Brasil
RISK_CATEGORIES = {
    "seguro":          {"nivel_padrao": "baixo",    "label": "Sem Risco"},
    "violencia":       {"nivel_padrao": "moderado", "label": "Violência e Conteúdo Gráfico"},
    "gambling":        {"nivel_padrao": "moderado", "label": "Loot Boxes e Apostas"},
    "grooming":        {"nivel_padrao": "alto",     "label": "Contato com Estranhos / Grooming"},
    "bullying":        {"nivel_padrao": "moderado", "label": "Cyberbullying e Assédio"},
    "conteudo_adulto": {"nivel_padrao": "alto",     "label": "Conteúdo Sexual / Adulto"},
    "microtransacao":  {"nivel_padrao": "baixo",    "label": "Pressão para Gastar"},
    "fomo":            {"nivel_padrao": "baixo",    "label": "Mecânicas de Retenção / FOMO"},
    "extremismo":      {"nivel_padrao": "alto",     "label": "Conteúdo Extremista / Ódio"},
    "privacidade":     {"nivel_padrao": "moderado", "label": "Coleta de Dados / Privacidade"},
    "vicio":           {"nivel_padrao": "moderado", "label": "Padrões de Dependência"},
}

RISK_INFO = {
    "violencia": {
        "descricao_risco": "Conteúdo com armas, sangue, morte ou combate realista detectado na tela.",
        "pode_ser": [
            "Cenas de combate com representação gráfica de violência",
            "Uso de armas realistas no jogo",
            "Conteúdo perturbador como morte ou sangue visível",
        ],
        "recomendacoes": [
            "Converse com seu filho sobre a diferença entre ficção e realidade",
            "Verifique a classificação etária do jogo (PEGI/ESRB)",
            "Considere limitar o tempo diário neste jogo",
        ],
    },
    "gambling": {
        "descricao_risco": "Mecânicas de loot boxes, apostas ou recompensas aleatórias pagas detectadas.",
        "pode_ser": [
            "Caixas mistério com recompensas aleatórias pagas",
            "Roletas, sorteios ou sistemas de probabilidade",
            "Moeda premium com conversão de dinheiro real",
        ],
        "recomendacoes": [
            "Desative compras dentro do aplicativo nas configurações do dispositivo",
            "Explique ao seu filho como esses sistemas funcionam como apostas",
            "A ECA Digital (Lei 15.211/2025) proíbe loot boxes para menores — você pode reportar o app",
        ],
    },
    "grooming": {
        "descricao_risco": "Possível contato suspeito de adulto desconhecido detectado.",
        "pode_ser": [
            "Adulto pedindo para continuar conversa em outro aplicativo",
            "Pedido de informações pessoais como nome, escola ou endereço",
            "Solicitação de fotos ou vídeos da criança",
        ],
        "recomendacoes": [
            "Converse com seu filho imediatamente sobre esse contato",
            "Oriente a nunca compartilhar informações pessoais com desconhecidos",
            "Registre uma denúncia no SaferNet Brasil (safernet.org.br) ou Delegacia Online",
            "Considere bloquear o chat neste jogo temporariamente",
        ],
    },
    "bullying": {
        "descricao_risco": "Mensagens de ódio, ofensas ou comportamento tóxico detectados.",
        "pode_ser": [
            "Insultos e xingamentos direcionados ao jogador",
            "Exclusão coordenada ou isolamento no jogo",
            "Comentários discriminatórios ou assédio persistente",
        ],
        "recomendacoes": [
            "Pergunte ao seu filho como ele se sente ao jogar esse jogo",
            "Ensine a usar as ferramentas de bloqueio e denúncia do jogo",
            "Se persistir, considere pausar esse jogo por um tempo",
        ],
    },
    "conteudo_adulto": {
        "descricao_risco": "Conteúdo sexual, impróprio ou roleplay adulto detectado na tela.",
        "pode_ser": [
            "Imagens ou animações de cunho sexual",
            "Linguagem explicitamente sexual no chat",
            "Jogos de roleplay com temática adulta dentro da plataforma",
        ],
        "recomendacoes": [
            "Remova imediatamente o jogo ou bloqueie o acesso",
            "Converse abertamente com seu filho sobre o que foi visto",
            "Denuncie o conteúdo diretamente na plataforma do jogo",
        ],
    },
    "microtransacao": {
        "descricao_risco": "Pressão de compra com timers de urgência ou itens limitados detectada.",
        "pode_ser": [
            "Mensagens de urgência como 'oferta expira em X horas'",
            "Itens exclusivos com prazo para compra",
            "Design manipulador para incentivar gastos imediatos",
        ],
        "recomendacoes": [
            "Combine com seu filho um valor mensal máximo para jogos",
            "Explique que itens 'exclusivos' são uma estratégia de marketing",
            "Desative cartões de crédito vinculados à conta do jogo",
        ],
    },
    "fomo": {
        "descricao_risco": "Mecânicas de retenção criando ansiedade por não jogar detectadas.",
        "pode_ser": [
            "Recompensas diárias que exigem login obrigatório",
            "Eventos sazonais que expiram e pressionam o retorno",
            "Progressão perdida por não jogar por um dia",
        ],
        "recomendacoes": [
            "Estabeleça horários fixos de jogo para reduzir a ansiedade",
            "Explique que perder uma recompensa virtual não é um problema real",
            "Observe se seu filho demonstra ansiedade quando não pode jogar",
        ],
    },
    "extremismo": {
        "descricao_risco": "Conteúdo extremista, símbolos de ódio ou radicalização detectados.",
        "pode_ser": [
            "Símbolos ou linguagem de grupos extremistas",
            "Recriações de ataques terroristas ou atiradores",
            "Conteúdo de recrutamento de grupos radicais",
        ],
        "recomendacoes": [
            "Remova o jogo imediatamente",
            "Converse com seu filho sobre o que foi visto",
            "Denuncie na SaferNet Brasil e na plataforma do jogo",
            "Se necessário, busque orientação de um psicólogo",
        ],
    },
    "privacidade": {
        "descricao_risco": "Solicitação de dados pessoais ou permissões suspeitas detectadas.",
        "pode_ser": [
            "Pedido de localização, câmera ou microfone sem necessidade clara",
            "Formulário pedindo nome completo, escola ou data de nascimento",
            "Integração com redes sociais pedindo acesso aos contatos",
        ],
        "recomendacoes": [
            "Revise as permissões do jogo nas configurações do Android",
            "Oriente seu filho a nunca preencher dados pessoais em jogos",
            "Verifique a política de privacidade do jogo",
        ],
    },
    "vicio": {
        "descricao_risco": "Padrões de uso compulsivo ou sinais de dependência detectados.",
        "pode_ser": [
            "Jogo por períodos muito longos sem pausas",
            "Sinais de jogar por ansiedade e não por diversão",
            "Dificuldade em parar mesmo quando solicitado",
        ],
        "recomendacoes": [
            "Estabeleça limites de tempo claros e consistentes",
            "Inclua atividades físicas e sociais na rotina",
            "Se os padrões persistirem, consulte um pediatra ou psicólogo",
            "A OMS reconhece o Gaming Disorder (CID-11) como condição de saúde",
        ],
    },
    "seguro": {
        "descricao_risco": "Nenhum risco detectado nesta captura.",
        "pode_ser": ["Conteúdo adequado para a faixa etária"],
        "recomendacoes": ["Continue monitorando regularmente."],
    },
}

NIVEL_MAP = {
    "baixo":    "safe",
    "moderado": "attention",
    "alto":     "high_risk",
}

SYSTEM_PROMPT = """
Você é um agente de proteção digital infantil. Analise a captura de tela de um jogo
e classifique o conteúdo com base nas categorias de risco estabelecidas por
PEGI 2026, ESRB, WHO ICD-11, ECA Digital (Lei 15.211/2025) e SaferNet Brasil.

Categorias disponíveis:
- seguro: nenhum risco detectado
- violencia: armas, sangue, morte, combate gráfico realista
- gambling: loot boxes, apostas, recompensas aleatórias pagas, odds
- grooming: adulto pedindo contato externo, dados pessoais, fotos
- bullying: insultos, assédio, mensagens de ódio, exclusão
- conteudo_adulto: imagens sexuais, linguagem adulta, roleplay sexual
- microtransacao: timers de urgência, itens limitados, pressão de compra
- fomo: recompensas diárias obrigatórias, eventos expirando, ansiedade de não jogar
- extremismo: símbolos de ódio, conteúdo radical, recrutamento
- privacidade: pedido de dados pessoais, câmera, localização desnecessária
- vicio: padrões de uso compulsivo, incapacidade de parar

Responda APENAS em JSON válido (sem markdown):
{{
  "categoria": "uma das categorias acima",
  "nivel": "baixo|moderado|alto",
  "descricao": "descrição curta em português do que foi detectado na tela",
  "confianca": 0.0
}}

Se houver mais de um risco, classifique pelo mais grave.
"""

MOCK_REPORT_RAW = {
    "categoria": "seguro",
    "nivel":     "baixo",
    "descricao": "Conteúdo adequado para a faixa etária — nenhum risco detectado (mock)",
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
    "Converse abertamente com seu filho sobre os jogos que ele acessa.",
    "Estabeleça horários combinados para uso do celular, especialmente antes de dormir.",
    "Inclua atividades offline e físicas na rotina para equilibrar o tempo de tela.",
]


def _build_response(raw: dict, app_package: str) -> dict:
    categoria = raw.get("categoria", "seguro")
    nivel = raw.get("nivel", "baixo")
    info = RISK_INFO.get(categoria, RISK_INFO["seguro"])
    return {
        "app":               app_package or "desconhecido",
        "categoria":         categoria,
        "categoria_label":   RISK_CATEGORIES.get(categoria, {}).get("label", categoria),
        "nivel":             nivel,
        "risk_level":        NIVEL_MAP.get(nivel, "safe"),
        "descricao":         raw.get("descricao", ""),
        "confianca":         raw.get("confianca", 0.0),
        "pode_ser":          info["pode_ser"],
        "recomendacoes":     info["recomendacoes"],
        "timestamp":         datetime.now(timezone.utc).isoformat(),
        "imagem_armazenada": False,
        "analise":           "gemini-2.5-flash",
    }


def analyze_image(image_bytes: bytes, app_package: str = "") -> dict:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return _build_response(MOCK_REPORT_RAW, app_package)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                SYSTEM_PROMPT,
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


def get_risk_info(categoria: str) -> dict:
    return RISK_INFO.get(categoria, RISK_INFO["seguro"])


def generate_recommendations(child_name: str, alerts: list[dict]) -> list[str]:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return MOCK_RECOMMENDATIONS

    try:
        from google import genai

        alerts_summary = "\n".join(
            f"- [{a.get('nivel', a.get('risk_level', '?'))}] {a.get('description', '')} "
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
